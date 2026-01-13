"""
미니게임 봇 모듈
가위바위보, 주사위, 예측 게임 등
"""

import random
import json
from datetime import datetime
from collections import defaultdict


class MinigameBot:
    """미니게임 봇 클래스"""
    
    def __init__(self, config_path="config.json"):
        """
        초기화
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 게임 히스토리
        self.game_history = []
        
        # 사용자별 게임 통계
        self.user_stats = defaultdict(lambda: {
            'rps_wins': 0,
            'rps_losses': 0,
            'rps_draws': 0,
            'dice_rolls': 0,
            'predictions': 0,
            'prediction_wins': 0
        })
        
        # 가위바위보 선택지
        self.rps_choices = ['가위', '바위', '보', 'rock', 'paper', 'scissors']
        
        print("[MinigameBot] 초기화 완료")
    
    def play_rps(self, username, user_choice):
        """
        가위바위보 게임
        Args:
            username: 사용자명
            user_choice: 사용자 선택 (가위/바위/보)
        Returns:
            dict: 게임 결과
        """
        # 선택 정규화
        user_choice = user_choice.lower()
        
        # 한글/영어 변환
        choice_map = {
            '가위': 'scissors', 'ㄱㅇ': 'scissors',
            '바위': 'rock', 'ㅂㅇ': 'rock',
            '보': 'paper', 'ㅂ': 'paper',
            'scissors': 'scissors', 'rock': 'rock', 'paper': 'paper'
        }
        
        if user_choice not in choice_map:
            return {
                'success': False,
                'message': '올바른 선택이 아닙니다. (가위/바위/보)'
            }
        
        user_choice_normalized = choice_map[user_choice]
        
        # 봇 선택
        bot_choice = random.choice(['rock', 'paper', 'scissors'])
        
        # 승패 판정
        result = self._determine_rps_winner(user_choice_normalized, bot_choice)
        
        # 통계 업데이트
        if result == 'win':
            self.user_stats[username]['rps_wins'] += 1
        elif result == 'lose':
            self.user_stats[username]['rps_losses'] += 1
        else:
            self.user_stats[username]['rps_draws'] += 1
        
        # 히스토리 저장
        self._save_game_history('rps', username, {
            'user_choice': user_choice_normalized,
            'bot_choice': bot_choice,
            'result': result
        })
        
        # 한글 변환
        choice_kr = {'rock': '바위', 'paper': '보', 'scissors': '가위'}
        
        return {
            'success': True,
            'user_choice': choice_kr[user_choice_normalized],
            'bot_choice': choice_kr[bot_choice],
            'result': result,
            'message': self._get_rps_message(result, choice_kr[bot_choice])
        }
    
    def _determine_rps_winner(self, user, bot):
        """
        가위바위보 승패 판정
        Args:
            user: 사용자 선택
            bot: 봇 선택
        Returns:
            str: 결과 (win/lose/draw)
        """
        if user == bot:
            return 'draw'
        
        win_conditions = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }
        
        if win_conditions[user] == bot:
            return 'win'
        else:
            return 'lose'
    
    def _get_rps_message(self, result, bot_choice):
        """가위바위보 결과 메시지"""
        messages = {
            'win': f'봇: {bot_choice}! 🎉 축하합니다! 승리!',
            'lose': f'봇: {bot_choice}! 😢 아쉽지만 패배...',
            'draw': f'봇: {bot_choice}! 🤝 비겼습니다!'
        }
        return messages.get(result, '')
    
    def roll_dice(self, username, num_dice=1):
        """
        주사위 굴리기
        Args:
            username: 사용자명
            num_dice: 주사위 개수 (1-5)
        Returns:
            dict: 주사위 결과
        """
        if not 1 <= num_dice <= 5:
            return {
                'success': False,
                'message': '주사위는 1~5개까지 굴릴 수 있습니다.'
            }
        
        # 주사위 굴리기
        rolls = [random.randint(1, 6) for _ in range(num_dice)]
        total = sum(rolls)
        
        # 통계 업데이트
        self.user_stats[username]['dice_rolls'] += 1
        
        # 히스토리 저장
        self._save_game_history('dice', username, {
            'num_dice': num_dice,
            'rolls': rolls,
            'total': total
        })
        
        # 결과 메시지
        dice_emoji = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        dice_str = ' '.join(dice_emoji[r-1] for r in rolls)
        
        return {
            'success': True,
            'rolls': rolls,
            'total': total,
            'message': f'🎲 주사위: {dice_str} | 합계: {total}'
        }
    
    def random_pick(self, username, items):
        """
        랜덤 뽑기
        Args:
            username: 사용자명
            items: 선택지 리스트
        Returns:
            dict: 뽑기 결과
        """
        if not items or len(items) < 2:
            return {
                'success': False,
                'message': '최소 2개 이상의 선택지가 필요합니다.'
            }
        
        picked = random.choice(items)
        
        # 히스토리 저장
        self._save_game_history('random_pick', username, {
            'items': items,
            'picked': picked
        })
        
        return {
            'success': True,
            'picked': picked,
            'message': f'🎰 결과: {picked}'
        }
    
    def predict_game(self, username, prediction):
        """
        게임 결과 예측
        Args:
            username: 사용자명
            prediction: 예측 (win/lose)
        Returns:
            dict: 예측 등록 결과
        """
        prediction = prediction.lower()
        
        if prediction not in ['win', 'lose', '승리', '패배']:
            return {
                'success': False,
                'message': '올바른 예측이 아닙니다. (승리/패배)'
            }
        
        # 정규화
        pred_normalized = 'win' if prediction in ['win', '승리'] else 'lose'
        
        # 통계 업데이트
        self.user_stats[username]['predictions'] += 1
        
        # 예측 저장
        self._save_game_history('prediction', username, {
            'prediction': pred_normalized,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'success': True,
            'prediction': pred_normalized,
            'message': f'🔮 예측 등록됨: {"승리" if pred_normalized == "win" else "패배"}'
        }
    
    def resolve_predictions(self, actual_result):
        """
        예측 결과 처리
        Args:
            actual_result: 실제 결과 (win/lose)
        Returns:
            dict: 예측 맞춘 사용자 목록
        """
        winners = []
        
        # 최근 예측 조회
        recent_predictions = [
            game for game in self.game_history
            if game['game_type'] == 'prediction'
        ][-50:]  # 최근 50개
        
        for pred in recent_predictions:
            if pred['data']['prediction'] == actual_result:
                username = pred['username']
                winners.append(username)
                self.user_stats[username]['prediction_wins'] += 1
        
        return {
            'actual_result': actual_result,
            'winners': winners,
            'total_predictions': len(recent_predictions),
            'win_count': len(winners)
        }
    
    def get_user_stats(self, username):
        """
        사용자 게임 통계 조회
        Args:
            username: 사용자명
        Returns:
            dict: 통계 데이터
        """
        stats = self.user_stats.get(username, {})
        
        # 가위바위보 승률 계산
        rps_total = stats.get('rps_wins', 0) + stats.get('rps_losses', 0) + stats.get('rps_draws', 0)
        rps_winrate = (stats.get('rps_wins', 0) / rps_total * 100) if rps_total > 0 else 0
        
        # 예측 정확도
        pred_total = stats.get('predictions', 0)
        pred_accuracy = (stats.get('prediction_wins', 0) / pred_total * 100) if pred_total > 0 else 0
        
        return {
            'username': username,
            'rps': {
                'wins': stats.get('rps_wins', 0),
                'losses': stats.get('rps_losses', 0),
                'draws': stats.get('rps_draws', 0),
                'winrate': round(rps_winrate, 2)
            },
            'dice_rolls': stats.get('dice_rolls', 0),
            'predictions': {
                'total': pred_total,
                'wins': stats.get('prediction_wins', 0),
                'accuracy': round(pred_accuracy, 2)
            }
        }
    
    def _save_game_history(self, game_type, username, data):
        """게임 히스토리 저장"""
        self.game_history.append({
            'game_type': game_type,
            'username': username,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        
        # 히스토리 크기 제한 (최근 1000개)
        if len(self.game_history) > 1000:
            self.game_history = self.game_history[-1000:]
    
    def get_leaderboard(self, game_type='rps', limit=10):
        """
        리더보드 조회
        Args:
            game_type: 게임 타입 (rps/dice/prediction)
            limit: 표시할 순위 수
        Returns:
            list: 리더보드
        """
        if game_type == 'rps':
            # 가위바위보 승수 기준
            leaderboard = sorted(
                [(user, stats['rps_wins']) for user, stats in self.user_stats.items()],
                key=lambda x: x[1],
                reverse=True
            )
        elif game_type == 'prediction':
            # 예측 맞춘 횟수 기준
            leaderboard = sorted(
                [(user, stats['prediction_wins']) for user, stats in self.user_stats.items()],
                key=lambda x: x[1],
                reverse=True
            )
        else:
            return []
        
        return leaderboard[:limit]
