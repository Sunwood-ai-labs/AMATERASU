# ECRを使用したFargateイメージ更新PowerShellスクリプト

# 変数設定
$region = "ap-northeast-1"
$accountId = "498218886114"
$ecrRepo = "prompt-pandora"
$imageTag = "latest"
$ecrUri = "${accountId}.dkr.ecr.${region}.amazonaws.com"
$imageName = "${ecrUri}/${ecrRepo}:${imageTag}"
$clusterName = "prompt-pandora-cluster"
$serviceName = "prompt-pandora-service"

# エラーが発生した場合にスクリプトを停止
$ErrorActionPreference = "Stop"

try {

    # 2. ECRにログイン
    Write-Host "ECRにログインしています..."
    aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $ecrUri


    aws ecr create-repository --repository-name ${ecrRepo} --region $region

    # 1. 新しいDockerイメージをビルド
    Write-Host "Dockerイメージをビルドしています..."
    docker build -t ${ecrRepo}:$imageTag .


    # 3. イメージにECRリポジトリのタグを付ける
    Write-Host "イメージにタグを付けています..."
    docker tag ${ecrRepo}:$imageTag $imageName

    # 4. ECRにイメージをプッシュ
    Write-Host "イメージをECRにプッシュしています..."
    docker push $imageName

    # 5. ECSサービスを強制的に新しいデプロイメントにする
    Write-Host "ECSサービスを更新しています..."
    aws ecs update-service --cluster $clusterName --service $serviceName --force-new-deployment

    # 6. デプロイの状態を確認
    Write-Host "デプロイの状態を確認しています..."
    aws ecs describe-services --cluster $clusterName --services $serviceName

    Write-Host "更新プロセスが完了しました。"
}
catch {
    Write-Host "エラーが発生しました: $_"
    exit 1
}
