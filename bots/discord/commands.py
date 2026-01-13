"""
디스코드 봇 명령어 시스템
Custom commands management
"""
import json
import os
from typing import Dict, List


class CommandManager:
    """커스텀 명령어 관리 클래스"""
    
    def __init__(self, commands_file='custom_commands.json'):
        self.commands_file = commands_file
        self.commands: Dict[str, str] = {}
        self.load_commands()
    
    def load_commands(self):
        """명령어 파일에서 로드"""
        if os.path.exists(self.commands_file):
            try:
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    self.commands = json.load(f)
            except Exception as e:
                print(f'명령어 로드 오류: {str(e)}')
                self.commands = {}
        else:
            self.commands = {}
    
    def save_commands(self):
        """명령어 파일에 저장"""
        try:
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(self.commands, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'명령어 저장 오류: {str(e)}')
            return False
    
    def add_command(self, command_name: str, response: str) -> bool:
        """명령어 추가"""
        self.commands[command_name] = response
        return self.save_commands()
    
    def remove_command(self, command_name: str) -> bool:
        """명령어 제거"""
        if command_name in self.commands:
            del self.commands[command_name]
            return self.save_commands()
        return False
    
    def get_command(self, command_name: str) -> str:
        """명령어 응답 가져오기"""
        return self.commands.get(command_name, None)
    
    def list_commands(self) -> List[tuple]:
        """모든 명령어 리스트"""
        return [(cmd, resp) for cmd, resp in self.commands.items()]
    
    def command_exists(self, command_name: str) -> bool:
        """명령어 존재 여부"""
        return command_name in self.commands


# 기본 명령어 응답 템플릿
DEFAULT_COMMANDS = {
    '안녕': '안녕하세요! 무엇을 도와드릴까요?',
    '도움말': '사용 가능한 명령어: !안녕, !날씨, !주사위, !투표',
    '정보': '이 봇은 다기능 디스코드 봇입니다.',
}


if __name__ == '__main__':
    # 테스트
    manager = CommandManager()
    print(f"로드된 명령어 수: {len(manager.commands)}")
