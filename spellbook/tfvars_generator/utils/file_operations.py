"""
ファイル操作に関するユーティリティ関数を提供するモジュール
"""
import os
import shutil
import streamlit as st

def create_directory_if_not_exists(path):
    """
    指定されたパスにディレクトリが存在しない場合、ディレクトリを作成

    Args:
        path (str): 作成するディレクトリのパス
    """
    if not os.path.exists(path):
        os.makedirs(path)

def write_tfvars(project, content):
    """
    指定されたプロジェクトのterraform.tfvarsファイルを生成

    Args:
        project (dict): プロジェクト情報 (name, pathを含む)
        content (str): terraform.tfvarsファイルの内容
    """
    dir_path = os.path.dirname(project['path'])
    create_directory_if_not_exists(dir_path)
    
    try:
        with open(project['path'], 'w') as f:
            f.write(content)
        st.success(f"✅ Generated for {project['name']}: {project['path']}")
    except Exception as e:
        st.error(f"❌ Error generating for {project['name']}: {str(e)}")

def delete_terraform_cache(project_path):
    """
    Terraformのキャッシュファイルを削除

    Args:
        project_path (str): terraform.tfvarsファイルのパス
    
    Returns:
        bool: 削除が成功したかどうか
    """
    try:
        # プロジェクトのディレクトリパスを取得
        dir_path = os.path.dirname(project_path)
        
        # 進捗表示用のコンテナ
        st.markdown("### 🔄 キャッシュ削除の進捗")
        progress_container = st.container()
        
        # ログ表示用のコンテナ
        st.markdown("### 📝 処理ログ")
        log_container = st.container()
        
        with log_container:
            st.write("🔍 キャッシュ削除を開始します")
            st.code(f"対象ディレクトリ: {dir_path}")
        
        # 削除対象のファイル・ディレクトリ
        cache_paths = {
            '.terraform': os.path.join(dir_path, '.terraform'),
            'terraform.tfstate': os.path.join(dir_path, 'terraform.tfstate'),
            'terraform.tfstate.backup': os.path.join(dir_path, 'terraform.tfstate.backup'),
            '.terraform.lock.hcl': os.path.join(dir_path, '.terraform.lock.hcl')
        }
        
        deleted_files = []
        skipped_files = []
        total_files = len(cache_paths)
        current_file = 0
        
        # キャッシュの削除
        for name, path in cache_paths.items():
            current_file += 1
            
            # 進捗状況の更新
            with progress_container:
                st.progress(current_file / total_files)
                st.write(f"⏳ 処理中: {name} ({current_file}/{total_files})")
            
            if os.path.exists(path):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        deleted_files.append((name, path, "directory"))
                        with log_container:
                            st.write(f"📂 ディレクトリを削除: {path}")
                    else:
                        os.remove(path)
                        deleted_files.append((name, path, "file"))
                        with log_container:
                            st.write(f"📄 ファイルを削除: {path}")
                except Exception as e:
                    error_msg = f"❌ {path}の削除に失敗しました: {str(e)}"
                    with log_container:
                        st.error(error_msg)
                    return False
            else:
                skipped_files.append((name, path))
                with log_container:
                    st.write(f"⏭️ 存在しないためスキップ: {path}")
        
        # 最終的な進捗表示を更新
        with progress_container:
            st.progress(1.0)
            st.write("✅ 処理完了")
        
        # 削除結果の詳細表示
        with st.expander("📊 削除結果の詳細", expanded=True):
            if deleted_files:
                st.success("✅ 削除したキャッシュ:")
                for name, path, type_info in deleted_files:
                    icon = "📂" if type_info == "directory" else "📄"
                    st.code(f"{icon} {name}\n└─ {path}")
            
            if skipped_files:
                st.info("⏭️ スキップしたファイル:")
                for name, path in skipped_files:
                    st.code(f"🚫 {name}\n└─ {path}")
            
            st.success(f"""
            ### ✨ 処理サマリー
            - ✅ 削除成功: {len(deleted_files)}件
            - ⏭️ スキップ: {len(skipped_files)}件
            - 📁 対象ディレクトリ: {dir_path}
            """)
        
        return True
        
    except Exception as e:
        st.error(f"❌ キャッシュ削除でエラーが発生しました: {str(e)}")
        return False
