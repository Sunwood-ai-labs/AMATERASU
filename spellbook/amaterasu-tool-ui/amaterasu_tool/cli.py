"""
Amaterasu Tool CLI - AWSインフラストラクチャ設定管理CLIツール
"""
import argparse
import os
from amaterasu_tool.config.terraform import TerraformConfig
from amaterasu_tool.utils.project import ProjectDiscovery

class AmaterasuCLI:
    def __init__(self):
        """CLIツールの初期化"""
        self.parser = self._create_parser()
        self.terraform_config = TerraformConfig()
        self.project_discovery = ProjectDiscovery()

    def _create_parser(self) -> argparse.ArgumentParser:
        """コマンドライン引数パーサーの作成"""
        parser = argparse.ArgumentParser(
            description="Amaterasu Tool - AWSインフラストラクチャ設定管理ツール"
        )

        parser.add_argument(
            "--base-path",
            default="/home/maki/prj/AMATERASU/spellbook",
            help="spellbookのベースディレクトリパス"
        )
        
        parser.add_argument(
            "--output-json",
            default="base-infrastructure/output.json",
            help="base-infrastructureのoutput.jsonへのパス（ベースパスからの相対パス）"
        )

        parser.add_argument(
            "--project-dir",
            help="特定のプロジェクトディレクトリを指定（指定しない場合は全プロジェクトを処理）"
        )

        parser.add_argument(
            "--aws-region",
            default="ap-northeast-1",
            help="AWSリージョン"
        )

        parser.add_argument(
            "--instance-type",
            default="t3.medium",
            help="EC2インスタンスタイプ"
        )

        parser.add_argument(
            "--ami-id",
            default="ami-0d52744d6551d851e",
            help="AMI ID"
        )

        parser.add_argument(
            "--project-prefix",
            default="amts-",
            help="プロジェクト名のプレフィックス（デフォルト: amts-）"
        )

        parser.add_argument(
            "--key-name",
            required=True,
            help="SSH キーペア名"
        )

        return parser

    def run(self):
        """CLIツールの実行"""
        args = self.parser.parse_args()

        # output.jsonの読み込み
        output_json = self.terraform_config.load_output_json(
            args.base_path,
            args.output_json
        )

        # プロジェクトの探索
        projects = self.project_discovery.find_projects(
            args.base_path,
            args.project_dir
        )

        if not projects:
            print("⚠️ 対象となるプロジェクトが見つかりませんでした")
            return

        # 各プロジェクトに対してterraform.tfvarsを生成
        for project in projects:
            # main-infrastructure の terraform.tfvars を生成
            tfvars_path = self.project_discovery.get_tfvars_path(
                args.base_path,
                project
            )

            content = self.terraform_config.generate_tfvars_content(
                project_name=project,
                project_prefix=args.project_prefix,
                output_json=output_json,
                aws_region=args.aws_region,
                instance_type=args.instance_type,
                ami_id=args.ami_id,
                key_name=args.key_name
            )

            try:
                os.makedirs(os.path.dirname(tfvars_path), exist_ok=True)
                with open(tfvars_path, 'w') as f:
                    f.write(content)
                print(f"✅ Generated terraform.tfvars for {project}: {tfvars_path}")
            except Exception as e:
                print(f"❌ Error generating for {project}: {str(e)}")
            
            # cloudfront-infrastructure の terraform.tfvars を生成
            cloudfront_tfvars_path = self.project_discovery.get_cloudfront_tfvars_path(
                args.base_path,
                project
            )
            
            cloudfront_content = self.terraform_config.generate_cloudfront_tfvars_content(
                project_name=project,
                project_prefix=args.project_prefix,
                output_json=output_json,
                aws_region=args.aws_region,
            )
            
            try:
                os.makedirs(os.path.dirname(cloudfront_tfvars_path), exist_ok=True)
                with open(cloudfront_tfvars_path, 'w') as f:
                    f.write(cloudfront_content)
                print(f"✅ Generated cloudfront terraform.tfvars for {project}: {cloudfront_tfvars_path}")
            except Exception as e:
                print(f"❌ Error generating cloudfront for {project}: {str(e)}")

def main():
    """CLIのエントリーポイント"""
    cli = AmaterasuCLI()
    cli.run()

if __name__ == "__main__":
    main()
