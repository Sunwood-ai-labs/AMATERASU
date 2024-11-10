import sys

def visualize_invisible_chars(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 空白文字を可視化
    content = content.replace(' ', '·')
    # タブを可視化
    content = content.replace('\t', '→   ')
    # 改行を可視化
    content = content.replace('\n', '↵\n')
    # キャリッジリターンを可視化
    content = content.replace('\r', '←')
    
    print(f"Visualized content of {filename}:")
    print(content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    visualize_invisible_chars(sys.argv[1])
