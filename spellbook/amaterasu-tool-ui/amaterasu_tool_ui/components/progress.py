"""
進捗表示のUIコンポーネントを提供するモジュール
"""
import gradio as gr
from typing import Dict, Any, List, Optional, Callable
import time

def show_progress(
    title: str,
    description: str = "",
    show_result: bool = True
) -> tuple[gr.Blocks, Callable[[int, int, str], None], Callable[[str, str], None]]:
    """
    進捗表示コンポーネントを作成

    Args:
        title (str): 進捗表示のタイトル
        description (str): 進捗の説明文
        show_result (bool): 結果表示を含めるかどうか

    Returns:
        tuple[gr.Blocks, Callable, Callable]: 
            - Gradioコンポーネント
            - 進捗更新関数 (current, total, message)
            - 結果表示関数 (status, message)
    """
    with gr.Blocks() as progress:
        gr.Markdown(f"## {title}")
        
        if description:
            gr.Markdown(description)
        
        # 進捗表示用のコンポーネント
        progress_bar = gr.Slider(
            minimum=0,
            maximum=100,
            value=0,
            label="進捗",
            interactive=False
        )
        status_text = gr.Markdown("⏳ 準備中...")
        
        # 結果表示用のコンポーネント
        if show_result:
            with gr.Accordion("📝 処理ログ", open=True):
                log_output = gr.Markdown("")
    
    def update_progress(current: int, total: int, message: str) -> None:
        """進捗を更新"""
        progress = min(current / total * 100, 100)
        progress_bar.update(progress)
        status_text.update(f"🔄 {message} ({current}/{total})")
    
    def show_result_message(status: str, message: str) -> None:
        """結果を表示"""
        if status == "success":
            status_text.update("✅ 処理が完了しました")
            if show_result:
                log_output.update(f"### ✨ 処理成功\n{message}")
        else:
            status_text.update("❌ エラーが発生しました")
            if show_result:
                log_output.update(f"### ⚠️ エラー\n{message}")
    
    return progress, update_progress, show_result_message

def show_file_generation_progress(
    projects: List[Dict[str, Any]],
    on_complete: Optional[Callable[[], None]] = None
) -> gr.Blocks:
    """
    ファイル生成の進捗を表示

    Args:
        projects (List[Dict[str, Any]]): 処理対象のプロジェクトリスト
        on_complete (Optional[Callable[[], None]]): 完了時のコールバック

    Returns:
        gr.Blocks: Gradioコンポーネント
    """
    progress, update_progress, show_result = show_progress(
        title="🔄 ファイル生成",
        description="terraform.tfvarsファイルを生成しています...",
        show_result=True
    )
    
    total_steps = len(projects) * 2  # main-infrastructureとcloudfront-infrastructure
    current_step = 0
    
    # main-infrastructureの生成
    for project in projects:
        current_step += 1
        update_progress(
            current_step,
            total_steps,
            f"main-infrastructure: {project['name']}"
        )
        time.sleep(0.3)  # UIの動きを視覚化するための遅延
        
        # cloudfront-infrastructureの生成
        if project.get('cloudfront_tfvars_path'):
            current_step += 1
            update_progress(
                current_step,
                total_steps,
                f"cloudfront-infrastructure: {project['name']}"
            )
            time.sleep(0.3)  # UIの動きを視覚化するための遅延
    
    show_result(
        "success",
        f"""
        🎉 以下のファイルが生成されました：
        
        - ✅ Main Infrastructure: {len(projects)}個
        - ✅ CloudFront Infrastructure: {sum(1 for p in projects if p.get('cloudfront_tfvars_path'))}個
        """
    )
    
    if on_complete:
        on_complete()
    
    return progress

def show_cache_cleaning_progress(
    projects: List[Dict[str, Any]],
    on_complete: Optional[Callable[[], None]] = None
) -> gr.Blocks:
    """
    キャッシュ削除の進捗を表示

    Args:
        projects (List[Dict[str, Any]]): 処理対象のプロジェクトリスト
        on_complete (Optional[Callable[[], None]]): 完了時のコールバック

    Returns:
        gr.Blocks: Gradioコンポーネント
    """
    progress, update_progress, show_result = show_progress(
        title="🧹 キャッシュ削除",
        description="Terraformのキャッシュを削除しています...",
        show_result=True
    )
    
    total_steps = len(projects)
    deleted_count = 0
    error_count = 0
    
    for i, project in enumerate(projects, 1):
        update_progress(i, total_steps, f"処理中: {project['name']}")
        
        try:
            # キャッシュ削除処理（ここでは仮の処理）
            time.sleep(0.3)  # UIの動きを視覚化するための遅延
            deleted_count += 1
        except Exception as e:
            error_count += 1
    
    show_result(
        "success" if error_count == 0 else "error",
        f"""
        🧹 キャッシュ削除結果：
        
        - ✅ 成功: {deleted_count}個
        - ❌ 失敗: {error_count}個
        """
    )
    
    if on_complete:
        on_complete()
    
    return progress
