# src/data_loader.py

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

class RatingDataset(Dataset):
    """
    사용자-아이템-평점 데이터를 파이토치 텐서 형태로 변환하는 커스텀 데이터셋
    """
    def __init__(self, users, items, ratings):
        self.users = users
        self.items = items
        self.ratings = ratings

    def __len__(self):
        return len(self.users)

    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.ratings[idx]

def extract_data(df, min_rating, user_count):
    """
    특정 조건에 맞는 데이터만 추출하여 학습 효율을 높입니다.
    
    Args:
        df (pd.DataFrame): 원본 평점 데이터프레임
        min_rating (float): 학습에 사용할 최소 평점 기준
        user_count (int): 분석에 포함할 최대 사용자 수
        
    Returns:
        pd.DataFrame: 필터링된 데이터프레임
    """
    top_users = df["user_id"].value_counts().reset_index().iloc[:user_count, :]
    filtered_data = df[(df['user_id'].isin(top_users['user_id'])) & (df['rating'] >= min_rating)]
    print(f"Original data length: {len(df)}, Filtered data length: {len(filtered_data)}")
    return filtered_data

def prepare_dataloaders(data_path, min_rating, user_count, batch_size, test_size, random_state):
    """
    데이터 로딩부터 DataLoader 생성까지 모든 데이터 준비 과정을 캡슐화합니다.
    
    Returns:
        tuple: (train_loader, test_loader, user_id_map, movie_id_map)
    """
    print("--- Preparing Data ---")
    # 1. 데이터 로드 및 필터링
    df = pd.read_pickle(data_path)
    df = extract_data(df, min_rating, user_count)

    # 2. ID 매핑
    user_id_map = {id: i for i, id in enumerate(df['user_id'].unique())}
    movie_id_map = {id: i for i, id in enumerate(df['movie_id'].unique())}
    df['user_idx'] = df['user_id'].map(user_id_map)
    df['movie_idx'] = df['movie_id'].map(movie_id_map)
    print("User and Movie IDs have been mapped to zero-based indices.")

    # 3. 데이터 분할
    train_data, test_data = train_test_split(df, test_size=test_size, random_state=random_state)
    print(f"Train data size: {len(train_data)}, Test data size: {len(test_data)}")

    # 4. 파이토치 데이터셋 및 데이터로더 생성
    train_dataset = RatingDataset(
        users=torch.LongTensor(train_data["user_idx"].values),
        items=torch.LongTensor(train_data["movie_idx"].values),
        ratings=torch.FloatTensor(train_data["rating"].values),
    )
    
    # 테스트 데이터셋은 평가 시에만 사용되므로 별도 DataLoader를 만들 필요는 없지만,
    # 일관성을 위해 만들거나 혹은 DataFrame 그대로 반환할 수 있습니다. 여기서는 후자를 택합니다.
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    print("--- Data Preparation Finished ---\
")
    return train_loader, test_data, user_id_map, movie_id_map
