import requests
import sys
from typing import List, Dict
import time

class GitLabLabelCreator:
    def __init__(self, private_token: str, gitlab_url: str):
        """
        GitLabのラベル作成クラスの初期化
        
        Args:
            private_token (str): GitLab Private Token
            gitlab_url (str): GitLabのURL
        """
        self.private_token = private_token
        self.gitlab_url = gitlab_url.rstrip('/')
        self.headers = {'PRIVATE-TOKEN': private_token}
        
    def get_group_projects(self, group_id: int) -> List[Dict]:
        """
        グループ内の全プロジェクトを取得
        
        Args:
            group_id (int): グループID
            
        Returns:
            List[Dict]: プロジェクト情報のリスト
        """
        projects = []
        page = 1
        while True:
            url = f"{self.gitlab_url}/api/v4/groups/{group_id}/projects"
            params = {'page': page, 'per_page': 100}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error getting projects: {response.status_code}")
                return []
                
            batch = response.json()
            if not batch:
                break
                
            projects.extend(batch)
            page += 1
            
        return projects
        
    def create_label(self, project_id: int, label_data: Dict) -> bool:
        """
        プロジェクトにラベルを作成
        
        Args:
            project_id (int): プロジェクトID
            label_data (Dict): ラベル情報
            
        Returns:
            bool: 作成成功でTrue
        """
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/labels"
        response = requests.post(url, headers=self.headers, json=label_data)
        
        if response.status_code == 201:
            return True
        elif response.status_code == 409:
            print(f"Label '{label_data['name']}' already exists in project {project_id}")
            return True
        else:
            print(f"Error creating label in project {project_id}: {response.status_code}")
            return False
            
    def create_labels_for_group(self, group_id: int, labels: List[Dict]) -> None:
        """
        グループ内の全プロジェクトにラベルを作成
        
        Args:
            group_id (int): グループID
            labels (List[Dict]): 作成するラベル情報のリスト
        """
        projects = self.get_group_projects(group_id)
        print(f"Found {len(projects)} projects in group {group_id}")
        
        for project in projects:
            print(f"\nProcessing project: {project['name']}")
            for label in labels:
                if self.create_label(project['id'], label):
                    print(f"Created/Updated label '{label['name']}' in {project['name']}")
                time.sleep(0.5)  # API rate limiting対策

def main():
    # 設定
    GITLAB_TOKEN    = "glpat-KpMd3Kb8QT_g29ydeWrL"
    GITLAB_URL      = "http://192.168.0.131"
    GROUP_ID        = 5
    
    # 作成したいラベルのリスト
    labels_to_create = [
        {
            "name": "bug",
            "color": "#FF0000",
            "description": "バグ修正"
        },
        {
            "name": "feature",
            "color": "#428BCA",
            "description": "新機能追加"
        },
        {
            "name": "documentation",
            "color": "#F0AD4E",
            "description": "ドキュメント関連"
        },
        {
            "name": "enhancement",
            "color": "#5CB85C",
            "description": "機能改善"
        },
        {
            "name": "question",
            "color": "#8E44AD",
            "description": "質問・問い合わせ"
        },
        {
            "name": "high-priority",
            "color": "#D9534F",
            "description": "優先度高"
        },
        {
            "name": "medium-priority",
            "color": "#F0AD4E",
            "description": "優先度中"
        },
        {
            "name": "low-priority",
            "color": "#5BC0DE",
            "description": "優先度低"
        }
    ]
    
    creator = GitLabLabelCreator(GITLAB_TOKEN, GITLAB_URL)
    creator.create_labels_for_group(GROUP_ID, labels_to_create)

if __name__ == "__main__":
    main()
