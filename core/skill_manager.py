import re
import yaml
import shutil
import zipfile
from pathlib import Path
from config import USER_SKILLS_DIR, SYSTEM_SKILLS_DIR


class SkillManager:
    def __init__(self):
        self.user_skills_dir = USER_SKILLS_DIR
        self.system_skills_dir = SYSTEM_SKILLS_DIR

    def scan_skills(self):
        skills = []
        skills.extend(self._scan_directory(self.user_skills_dir, 'user'))
        skills.extend(self._scan_directory(self.system_skills_dir, 'system'))
        return skills

    def _scan_directory(self, directory, location):
        skills = []
        if not directory.exists():
            return skills

        for skill_dir in directory.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / 'SKILL.md'
            if not skill_md.exists():
                continue

            metadata = self._parse_skill_md(skill_md)
            if metadata:
                allowed_tools = metadata.get('allowed-tools', '')
                if isinstance(allowed_tools, list):
                    allowed_tools = ', '.join(allowed_tools)

                skills.append({
                    'name': metadata.get('name', skill_dir.name),
                    'description': metadata.get('description', ''),
                    'version': metadata.get('version', '1.0.0'),
                    'location': location,
                    'path': str(skill_md),
                    'base_dir': str(skill_dir),
                    'enabled': not (skill_dir / '.disabled').exists(),
                    'user_invocable': metadata.get('user-invocable', False),
                    'argument_hint': metadata.get('argument-hint', ''),
                    'allowed_tools': allowed_tools,
                    'license': metadata.get('license', ''),
                    'author': metadata.get('metadata', {}).get('author', '') if isinstance(metadata.get('metadata'), dict) else ''
                })

        return skills

    def _parse_skill_md(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = r'^---\s*\n(.*?)\n---\s*\n'
            match = re.match(pattern, content, re.DOTALL)

            if match:
                yaml_content = match.group(1)
                return yaml.safe_load(yaml_content)
        except Exception:
            pass
        return None

    def read_skill_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ''

    def get_skill_metadata(self, skill):
        """获取完整的skill元数据"""
        metadata = {
            '名称': skill.get('name', ''),
            '描述': skill.get('description', ''),
            '版本': skill.get('version', ''),
            '位置': '用户' if skill.get('location') == 'user' else '系统',
            '状态': '启用' if skill.get('enabled', False) else '禁用',
            '用户可调用': '是' if skill.get('user_invocable', False) else '否',
            '参数提示': skill.get('argument_hint', ''),
            '允许的工具': skill.get('allowed_tools', ''),
            '许可证': skill.get('license', ''),
            '作者': skill.get('author', ''),
            '路径': skill.get('path', ''),
            '目录': skill.get('base_dir', '')
        }
        return metadata

    def toggle_skill(self, skill):
        try:
            base_dir = Path(skill['base_dir'])
            disabled_marker = base_dir / '.disabled'

            if disabled_marker.exists():
                disabled_marker.unlink()
            else:
                disabled_marker.touch()

            return True
        except Exception:
            return False

    def delete_skill(self, skill):
        try:
            if skill['location'] == 'system':
                return False

            base_dir = Path(skill['base_dir'])
            shutil.rmtree(base_dir)
            return True
        except Exception:
            return False

    def export_skill(self, skill, output_path):
        try:
            base_dir = Path(skill['base_dir'])
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in base_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(base_dir.parent)
                        zipf.write(file_path, arcname)
            return True
        except Exception:
            return False

    def import_skill(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(self.user_skills_dir)
            return True
        except Exception:
            return False
