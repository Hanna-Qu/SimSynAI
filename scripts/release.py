#!/usr/bin/env python3
"""
版本发布脚本

自动化版本管理流程：
1. 更新版本号
2. 生成变更日志
3. 创建Git标签
4. 推送到远程仓库
"""

import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path

class VersionManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.version_file = self.root_dir / "VERSION"
        self.changelog_file = self.root_dir / "CHANGELOG.md"
    
    def get_current_version(self):
        """获取当前版本"""
        if self.version_file.exists():
            return self.version_file.read_text().strip()
        return "0.0.0"
    
    def parse_version(self, version):
        """解析版本号"""
        parts = version.split('.')
        return {
            'major': int(parts[0]),
            'minor': int(parts[1]) if len(parts) > 1 else 0,
            'patch': int(parts[2]) if len(parts) > 2 else 0
        }
    
    def increment_version(self, current_version, bump_type):
        """递增版本号"""
        version = self.parse_version(current_version)
        
        if bump_type == 'major':
            version['major'] += 1
            version['minor'] = 0
            version['patch'] = 0
        elif bump_type == 'minor':
            version['minor'] += 1
            version['patch'] = 0
        elif bump_type == 'patch':
            version['patch'] += 1
        
        return f"{version['major']}.{version['minor']}.{version['patch']}"
    
    def update_version_file(self, new_version):
        """更新版本文件"""
        self.version_file.write_text(new_version)
        print(f"✅ 版本号已更新为: {new_version}")
    
    def update_changelog(self, version, changes):
        """更新变更日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if not self.changelog_file.exists():
            content = "# 变更日志\n\n"
        else:
            content = self.changelog_file.read_text()
        
        # 在第一个版本条目前插入新版本
        new_entry = f"## [{version}] - {today}\n\n{changes}\n\n"
        
        # 找到第一个版本条目的位置
        match = re.search(r'\n## \[', content)
        if match:
            pos = match.start() + 1
            content = content[:pos] + new_entry + content[pos:]
        else:
            content += new_entry
        
        self.changelog_file.write_text(content)
        print(f"✅ 变更日志已更新")
    
    def git_commit_and_tag(self, version, message):
        """提交更改并创建标签"""
        try:
            # 添加修改的文件
            subprocess.run(['git', 'add', str(self.version_file), str(self.changelog_file)], 
                         check=True, cwd=self.root_dir)
            
            # 提交更改
            commit_message = f"chore(release): 发布版本 {version}\n\n{message}"
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         check=True, cwd=self.root_dir)
            
            # 创建标签
            tag_message = f"发布版本 {version}"
            subprocess.run(['git', 'tag', '-a', f'v{version}', '-m', tag_message], 
                         check=True, cwd=self.root_dir)
            
            print(f"✅ Git提交和标签 v{version} 已创建")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git操作失败: {e}")
            return False
    
    def push_to_remote(self, version):
        """推送到远程仓库"""
        try:
            # 推送提交
            subprocess.run(['git', 'push'], check=True, cwd=self.root_dir)
            
            # 推送标签
            subprocess.run(['git', 'push', 'origin', f'v{version}'], 
                         check=True, cwd=self.root_dir)
            
            print(f"✅ 版本 {version} 已推送到远程仓库")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 推送失败: {e}")
            return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python release.py <major|minor|patch> [变更说明]")
        print("示例: python release.py minor '添加新功能'")
        sys.exit(1)
    
    bump_type = sys.argv[1].lower()
    if bump_type not in ['major', 'minor', 'patch']:
        print("❌ 版本类型必须是: major, minor, 或 patch")
        sys.exit(1)
    
    changes = sys.argv[2] if len(sys.argv) > 2 else "版本更新"
    
    vm = VersionManager()
    
    # 获取当前版本
    current_version = vm.get_current_version()
    print(f"📋 当前版本: {current_version}")
    
    # 计算新版本
    new_version = vm.increment_version(current_version, bump_type)
    print(f"🚀 新版本: {new_version}")
    
    # 确认发布
    confirm = input(f"确认发布版本 {new_version}? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ 发布已取消")
        sys.exit(0)
    
    # 更新版本文件
    vm.update_version_file(new_version)
    
    # 更新变更日志
    changelog_entry = f"""### 更改
- {changes}"""
    vm.update_changelog(new_version, changelog_entry)
    
    # Git提交和标签
    if not vm.git_commit_and_tag(new_version, changes):
        sys.exit(1)
    
    # 推送到远程仓库
    push = input("推送到远程仓库? (y/N): ")
    if push.lower() == 'y':
        if vm.push_to_remote(new_version):
            print(f"🎉 版本 {new_version} 发布成功!")
        else:
            print("❌ 推送失败，请手动推送")
    else:
        print(f"✅ 版本 {new_version} 准备完成，请手动推送")

if __name__ == "__main__":
    main() 