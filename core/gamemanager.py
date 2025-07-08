import pygame
from core.gamestate import GameState
from core.save_load import save_game, load_game
from core.stage_controller import StageController

class GameManager:
    """
    ゲーム全体の状態管理を行うクラス。
    スコア、ライフ、弾・レーザー管理、プレイヤー拘束、ステージ進行を統括。
    """
    # 定数設定
    INITIAL_LIVES = 3                # 初期ライフ数
    LASER_DURATION_MS = 2000         # レーザー持続時間（ミリ秒）
    LASER_SCORE_THRESHOLD = 100      # レーザー解放に必要なスコア閾値
    BULLET_COOLDOWN_NORMAL = 100     # 通常弾のクールダウン（ミリ秒）
    BULLET_COOLDOWN_SLOWED = 300     # 発射速度低下時のクールダウン
    RATE_DOWN_DURATION = 3000        # 発射速度低下持続時間（ミリ秒）

    def __init__(
        self,
        gm=None,
        all_sprites=None,
        enemies_group=None,
        spawn_enemy_func=None,
        fragment_image=None,
        fragment_group=None
    ):
        # デフォルト値を初期化
        self._setup_defaults()
        # ステージコントローラが指定されれば生成
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
        """
        コアとなるゲーム状態の初期値設定。
        リセットや初回起動時に利用。
        """
        # ゲーム状態
        self.state = GameState.START
        self.score = 0
        self.lives = self.INITIAL_LIVES
        self.bullet_type = 1

        # レーザー関連
        self.laser_score = 0                 # 解放ために貯めるスコア
        self.can_use_laser = False           # レーザー使用可能フラグ
        self.laser_gauge = 0                 # 表示用ゲージ値(0-100)
        self.laser_active = False            # レーザー発動中フラグ
        self._laser_start_time = 0           # レーザー発動時刻
        self._last_laser_end_time = -float('inf')  # 前回レーザー終了時刻
        self.score_since_last_laser = 0      # 前回レーザー以降の得点
        self._active_laser = None            # レーザーオブジェクト参照

        # 弾のクールダウン管理
        self.rate_down_active = False        # 発射速度低下中フラグ
        self._rate_down_start = 0            # 速度低下開始時刻
        self.bullet_cooldown = self.BULLET_COOLDOWN_NORMAL

        # プレイヤー拘束管理（特殊敵効果）
        self.player_bound = False
        self.bound_timer = 0

        # 経過時間管理
        self._start_ticks = pygame.time.get_ticks()
        self._pause_start = 0
        self._resume_offset = 0

        # ステージコントローラ格納
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
        """
        ゲーム再開始時に全データをクリアし、ステージコントローラを再生成する。
        """
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
        """
        弾のクールダウン時間を更新。
        RATE_DOWN_DURATION内はスロークールダウン、それ以外は通常クールダウンに戻す。
        """
        if self.rate_down_active and (now - self._rate_down_start < self.RATE_DOWN_DURATION):
            self.bullet_cooldown = self.BULLET_COOLDOWN_SLOWED
        else:
            self.rate_down_active = False
            self.bullet_cooldown = self.BULLET_COOLDOWN_NORMAL

    @property
    def elapsed_time(self):
        """
        経過時間をミリ秒で取得。
        GAMEOVER時は中断時刻を返す。
        """
        if self.state == GameState.GAMEOVER:
            return self._resume_offset
        return self._resume_offset + (pygame.time.get_ticks() - self._start_ticks)

    @property
    def minutes(self):
        """経過時間の分部分を取得。"""
        return self.elapsed_time // 60000

    @property
    def seconds(self):
        """経過時間の秒部分を取得。"""
        return (self.elapsed_time % 60000) // 1000

    @property
    def active_laser(self):
        """現在のレーザーオブジェクトを取得。"""
        return self._active_laser

    @active_laser.setter
    def active_laser(self, value):
        """レーザーオブジェクトを設定。"""
        self._active_laser = value

    @property
    def laser_start_time(self):
        """レーザー起動時のタイムスタンプを取得。"""
        return self._laser_start_time

    @property
    def laser_unlocked(self):
        """レーザーが解放済みかどうかを示すフラグ。"""
        return self.can_use_laser

    def add_laser_score(self, amount):
        """
        敵撃破等でスコアを追加し、閾値到達でレーザー解放状態にする。
        """
        if not self.can_use_laser:
            self.laser_score = min(self.LASER_SCORE_THRESHOLD, self.laser_score + amount)
            if self.laser_score >= self.LASER_SCORE_THRESHOLD:
                self.can_use_laser = True

    def activate_laser(self):
        """
        レーザー発動処理。
        発動中フラグ設定、タイムスタンプ記録、スコア蓄積リセット。
        """
        if self.can_use_laser:
            self.laser_active = True
            self._laser_start_time = pygame.time.get_ticks()
            self.score_since_last_laser = 0
            self.can_use_laser = False
            self.laser_score = 0

    def update_laser_gauge(self, dt=None):
        """
        レーザーゲージを更新。
        発動中は残り時間比率、それ以外は蓄積スコア値をゲージに反映。
        """
        now = pygame.time.get_ticks()
        if self.laser_active:
            elapsed = now - self._laser_start_time
            self.laser_gauge = max(0, 100 * (1 - elapsed / self.LASER_DURATION_MS))
            if elapsed >= self.LASER_DURATION_MS:
                # レーザー終了時処理
                self.laser_active = False
                self._last_laser_end_time = now
                self.score_since_last_laser = 0
                self.laser_gauge = 0
        else:
            self.laser_gauge = self.laser_score

    def add_score(self, amount):
        """
        スコア追加処理。
        前回レーザー終了以降の得点もカウント。
        """
        self.score += amount
        if self._last_laser_end_time > 0:
            self.score_since_last_laser += amount

    def pause(self):
        """ゲーム一時停止開始時刻を記録。"""
        self._pause_start = pygame.time.get_ticks()

    def resume(self):
        """
        一時停止解除時に経過時間補正。
        """
        now = pygame.time.get_ticks()
        self._resume_offset += now - self._pause_start

    def to_dict(self):
        """
        セーブ用に現在状態を辞書化。
        ステージスケジュールやゲージ等も含む。
        """
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
        """
        セーブデータ辞書から状態を復元。
        戻り値: 成功時True、例外時False
        """
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
            if self.stage_controller:
                self.stage_controller.schedule = data.get('schedule', [])
            return True
        except Exception:
            return False

    def save_to_file(self):
        """現在状態をファイルに保存。"""
        save_game(self.to_dict())

    def load_from_file(self):
        """
        ファイルからセーブデータを読み込み、復元処理を実行。
        戻り値: データなしFalse、復元結果True/False
        """
        data = load_game()
        if not data:
            return False
        return self.load_from_dict(data)
