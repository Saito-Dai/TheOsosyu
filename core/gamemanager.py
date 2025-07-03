import pygame
from core.gamestate import GameState
from core.save_load import save_game, load_game
from core.stage_controller import StageController

class GameManager:
    """ゲーム状態、スコア、レーザー、プレイヤー拘束、およびステージコントローラを管理します。"""
    INITIAL_LIVES = 3
    LASER_DURATION_MS = 2000
    LASER_SCORE_THRESHOLD = 100
    BULLET_COOLDOWN_NORMAL = 100
    BULLET_COOLDOWN_SLOWED = 300
    RATE_DOWN_DURATION = 3000

    def __init__(
        self,
        gm=None,
        all_sprites=None,
        enemies_group=None,
        spawn_enemy_func=None,
        fragment_image=None,
        fragment_group=None
    ):
        self._setup_defaults()
        if gm is not None:
            self.stage_controller = StageController(
                gm=gm,
                all_sprites=all_sprites,
                enemies_group=enemies_group,
                spawn_enemy_func=spawn_enemy_func,
                fragment_image=fragment_image,
                fragment_group=fragment_group
            )

    def _setup_defaults(self):
        # コアの状態
        self.state = GameState.START
        self.score = 0
        self.lives = self.INITIAL_LIVES
        self.bullet_type = 1

        # レーザー機能
        self.laser_score = 0             # レーザー解放のためのスコア蓄積
        self.can_use_laser = False       # レーザーが使用可能かどうか
        self.laser_gauge = 0             # ビジュアルゲージ値 (0-100)
        self.laser_active = False        # レーザー使用中フラグ
        self._laser_start_time = 0       # レーザー起動時のタイムスタンプ
        self._last_laser_end_time = -float('inf')
        self.score_since_last_laser = 0  # 最後のレーザー以降のスコア蓄積

        # レーザーオブジェクトプレースホルダ
        self._active_laser = None        # 現在のレーザーオブジェクト

        # 弾のクールダウン
        self.rate_down_active = False
        self._rate_down_start = 0
        self.bullet_cooldown = self.BULLET_COOLDOWN_NORMAL

        # プレイヤー拘束（Kabi効果用）
        self.player_bound = False
        self.bound_timer = 0

        # タイミング制御
        self._start_ticks = pygame.time.get_ticks()
        self._pause_start = 0
        self._resume_offset = 0

        # ステージコントローラのプレースホルダ
        self.stage_controller = None

    def reset(
        self,
        gm,
        all_sprites,
        enemies_group,
        spawn_enemy_func,
        fragment_image=None,
        fragment_group=None
    ):
        """すべてのゲームデータをリセットし、ステージコントローラを再生成します。"""
        self._setup_defaults()
        self.stage_controller = StageController(
            gm=gm,
            all_sprites=all_sprites,
            enemies_group=enemies_group,
            spawn_enemy_func=spawn_enemy_func,
            fragment_image=fragment_image,
            fragment_group=fragment_group
        )

    def update_bullet_cooldown(self, now):
        if self.rate_down_active and (now - self._rate_down_start < self.RATE_DOWN_DURATION):
            self.bullet_cooldown = self.BULLET_COOLDOWN_SLOWED
        else:
            self.rate_down_active = False
            self.bullet_cooldown = self.BULLET_COOLDOWN_NORMAL

    @property
    def elapsed_time(self):
        if self.state == GameState.GAMEOVER:
            return self._resume_offset
        return self._resume_offset + (pygame.time.get_ticks() - self._start_ticks)

    @property
    def minutes(self):
        return self.elapsed_time // 60000

    @property
    def seconds(self):
        return (self.elapsed_time % 60000) // 1000

    @property
    def active_laser(self):
        """現在のレーザーオブジェクトを取得または設定します。"""
        return self._active_laser

    @active_laser.setter
    def active_laser(self, value):
        self._active_laser = value

    @property
    def laser_start_time(self):
        """レーザー起動時のタイムスタンプです。"""
        return self._laser_start_time

    @property
    def laser_unlocked(self):
        """レーザーが解放され、起動準備ができているかどうかを示します。"""
        return self.can_use_laser

    def add_laser_score(self, amount):
        if not self.can_use_laser:
            self.laser_score = min(self.LASER_SCORE_THRESHOLD, self.laser_score + amount)
            if self.laser_score >= self.LASER_SCORE_THRESHOLD:
                self.can_use_laser = True

    def activate_laser(self):
        if self.can_use_laser:
            self.laser_active = True
            self._laser_start_time = pygame.time.get_ticks()
            self.score_since_last_laser = 0
            self.can_use_laser = False
            self.laser_score = 0

    def update_laser_gauge(self, dt=None):
        now = pygame.time.get_ticks()
        if self.laser_active:
            elapsed = now - self._laser_start_time
            self.laser_gauge = max(0, 100 * (1 - elapsed / self.LASER_DURATION_MS))
            if elapsed >= self.LASER_DURATION_MS:
                self.laser_active = False
                self._last_laser_end_time = now
                self.score_since_last_laser = 0
                self.laser_gauge = 0
        else:
            self.laser_gauge = self.laser_score

    def add_score(self, amount):
        self.score += amount
        if self._last_laser_end_time > 0:
            self.score_since_last_laser += amount

    def pause(self):
        self._pause_start = pygame.time.get_ticks()

    def resume(self):
        now = pygame.time.get_ticks()
        self._resume_offset += now - self._pause_start

    def to_dict(self):
        return {
            'score': self.score,
            'lives': self.lives,
            'bullet_type': self.bullet_type,
            'state': self.state.name,
            'elapsed_ms': self.elapsed_time,
            'resume_offset': self._resume_offset,
            'schedule': self.stage_controller.schedule if self.stage_controller else [],
            'laser_gauge': self.laser_gauge,
            'player_bound': self.player_bound,
            'bound_timer': self.bound_timer
        }

    def load_from_dict(self, data):
        try:
            self.score = data.get('score', 0)
            self.lives = data.get('lives', self.INITIAL_LIVES)
            self.bullet_type = data.get('bullet_type', 1)
            self.state = GameState[data.get('state', 'START')]
            self._resume_offset = data.get('resume_offset', 0)
            self._start_ticks = pygame.time.get_ticks()
            self.laser_gauge = data.get('laser_gauge', 0)
            self.player_bound = data.get('player_bound', False)
            self.bound_timer = data.get('bound_timer', 0)
            # レーザーオブジェクトは永続化しません
            if self.stage_controller:
                self.stage_controller.schedule = data.get('schedule', [])
            return True
        except Exception:
            return False

    def save_to_file(self):
        save_game(self.to_dict())

    def load_from_file(self):
        data = load_game()
        if not data:
            return False
        return self.load_from_dict(data)
