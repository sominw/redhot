import argparse

import pandas as pd
import numpy as np
from tqdm import tqdm
import praw
import re
import os

filter_char = lambda c: ord(c) < 256

sub_id_to_population_map = {
    "t5_2rtve": "lupus",
    "t5_2syer" : "gout",
    "t5_2s3g1" : "ibs",
    "t5_2tyg2" : "Psychosis",
    "t5_395ja" : "costochondritis",
    "t5_2saq9" : "POTS",
    "t5_2s23e" : "MultipleSclerosis",
    "t5_2s1h9" : "Epilepsy",
    "t5_2qlaa" : "GERD",
    "t5_2r876" : "CysticFibrosis",
    "t5_2tqwy" : "rheumatoidarthritis",
    "t5_2s453" : "IBD",
    "t5_2srfv" : "Dysthymia",
    "t5_2r4lw" : "CFS",
    "t5_2tmc8" : "bulimia",
    "t5_2rhx3" : "narcolepsy",
    "t5_2s0tv" : "Hypothyroidism",
    "t5_3e8dw" : "thyroidcancer",
    "t5_vqneh" : "Sinusitis",
    "t5_2rhwk" : "Hyperhidrosis",
    "t5_2qnwb" : "ADHD",
    "t5_2usbg" : "Gastroparesis",
    "t5_2qhsj" : "Diabetes",
    "t5_2tnlj" : "ankylosingspondylitis"
    }

parser = argparse.ArgumentParser(description="Intake Reddit Client ID & Secret, and file path to raw data files.")

parser.add_argument("--client_id", type=str, help="Reddit Client ID")
parser.add_argument("--client_secret", type=str, help="Reddit Client Secret")
parser.add_argument("--password", type=str, help="Reddit Password")
parser.add_argument("--user_agent", type=str, help="Reddit User Agent")
parser.add_argument("--username", type=str, help="Reddit Username")

parser.add_argument("--file_path", type=str, help="Path to raw data")

args = parser.parse_args()

reddit = praw.Reddit(
    client_id=args.client_id,
    client_secret=args.client_secret,
    password=args.password,
    user_agent=args.user_agent,
    username= args.username,
)

print ("Logged in as: " + reddit.user.me().name)

df = pd.read_csv(args.file_path, index_col=None)
url_format = "https://www.reddit.com/r/{}/comments/{}/"
posts = []
print ("Extracting posts...")
for _, row in tqdm(df.iterrows(), total=df.shape[0]):
    url = url_format.format(sub_id_to_population_map[row['subreddit_id']], row['post_id'])
    submission = reddit.submission(url=url)
    text = (submission.title.encode('utf-8') + b'\n' + submission.selftext.encode('utf-8')).decode("UTF-8")
    posts.append(text)

df["text"] = posts
df['text'] = df['text'].apply(lambda s: ''.join(filter(filter_char, s)))
df.to_csv(args.file_path.split(".csv")[0] + "_inc_text.csv", index=False)

print ("New dataframe generated: " + args.file_path.split(".csv")[0] + "_inc_text.csv.")