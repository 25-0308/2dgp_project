# ai_player.py
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_j, SDLK_k, SDLK_q, SDLK_w
import game_framework
from behavior_tree import BehaviorTree, Selector, Sequence, Condition, Action
import random


class AIPlayer:
    def __init__(self, player_object, difficulty='normal'):
        self.player = player_object
        self.target = None
        self.bt = None
        self.current_move_dir = None

        # AI 상태 관리
        self.action_cooldown = 0.0
        self.is_retreating = False  # 후퇴 중인지 상태 기억

        # 난이도 설정
        self.difficulty = difficulty
        self.set_difficulty_params()

        self.build_behavior_tree()

    def set_difficulty_params(self):
        """난이도별 파라미터 설정"""
        if self.difficulty == 'easy':
            self.reaction_time = 1.0  # 반응 속도 (느림) -> 행동 후 딜레이에 영향
            self.attack_distance = 180  # 공격 시작 거리
            self.approach_distance = 120  # 접근 멈춤 거리 (멀리서 멈춤)
            self.skill_use_chance = 0.2  # 스킬 사용 확률 (낮음)
        elif self.difficulty == 'hard':
            self.reaction_time = 0.2  # 반응 속도 (빠름)
            self.attack_distance = 160  # 공격 시작 거리
            self.approach_distance = 80  # 접근 멈춤 거리 (가까이 붙음)
            self.skill_use_chance = 0.6  # 스킬 사용 확률 (높음)
        else:  # normal
            self.reaction_time = 0.5  # 반응 속도 (보통)
            self.attack_distance = 170  # 공격 시작 거리
            self.approach_distance = 100  # 접근 멈춤 거리 (보통)
            self.skill_use_chance = 0.4  # 스킬 사용 확률 (보통)용 확률 (보통)

    def set_target(self, target):
        self.target = target

    def update(self):
        if self.target and self.player.hp > 0:
            self.action_cooldown -= game_framework.frame_time
            self.bt.run()

    # ==================== 조건 함수 ====================

    def is_action_ready(self):
        return BehaviorTree.SUCCESS if self.action_cooldown <= 0 else BehaviorTree.FAIL

    def should_use_skill(self):
        return BehaviorTree.SUCCESS if random.random() < self.skill_use_chance else BehaviorTree.FAIL

    def is_target_in_attack_range(self):
        if not self.target: return BehaviorTree.FAIL
        dist = abs(self.player.x - self.target.x)
        return BehaviorTree.SUCCESS if dist < self.attack_distance else BehaviorTree.FAIL

    def is_target_far(self):
        if not self.target: return BehaviorTree.FAIL
        dist = abs(self.player.x - self.target.x)
        return BehaviorTree.SUCCESS if dist > self.approach_distance else BehaviorTree.FAIL

    def is_target_jumping(self):
        if not self.target: return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS if self.target.y > 250 else BehaviorTree.FAIL

    def is_target_low_hp(self):
        if not self.target: return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS if self.target.hp <= 30 else BehaviorTree.FAIL

    def is_self_low_hp(self):
        # 체력 40 미만을 위험 상태로 고정
        return BehaviorTree.SUCCESS if self.player.hp < 40 else BehaviorTree.FAIL

    def should_retreat(self):
        # 이 함수는 더 이상 사용되지 않습니다.
        return BehaviorTree.FAIL

    # ==================== 행동 함수 ====================

    def move_toward_target(self):
        if not self.target or self.is_retreating:
            return BehaviorTree.FAIL

        dx = self.target.x - self.player.x
        dist = abs(dx)

        if dist < self.approach_distance:
            self.stop_moving()
            return BehaviorTree.SUCCESS

        new_dir = SDLK_RIGHT if dx > 0 else SDLK_LEFT
        if self.current_move_dir != new_dir:
            if self.current_move_dir:
                self.player.handle_event_simulate(SDL_KEYUP, self.current_move_dir)
            self.player.handle_event_simulate(SDL_KEYDOWN, new_dir)
            self.current_move_dir = new_dir
        return BehaviorTree.SUCCESS

    def move_away_from_target(self):
        if not self.target:
            self.is_retreating = False
            return BehaviorTree.FAIL

        self.is_retreating = True
        dx = self.target.x - self.player.x

        # 후퇴 방향을 결정하고 계속 그 방향으로 이동
        new_dir = SDLK_LEFT
        if self.current_move_dir != new_dir:
            if self.current_move_dir:
                self.player.handle_event_simulate(SDL_KEYUP, self.current_move_dir)
            self.player.handle_event_simulate(SDL_KEYDOWN, new_dir)
            self.current_move_dir = new_dir  # 올바른 방향 키 값으로 수정

        # 체력이 낮은 동안에는 멈추지 않고 계속 후퇴
        return BehaviorTree.SUCCESS

    def stop_moving(self):
        if self.current_move_dir:
            self.player.handle_event_simulate(SDL_KEYUP, self.current_move_dir)
            self.current_move_dir = None
        return BehaviorTree.SUCCESS

    def do_quick_punch(self):
        self.stop_moving()
        self.player.handle_event_simulate(SDL_KEYDOWN, SDLK_j)
        self.player.handle_event_simulate(SDL_KEYUP, SDLK_j)
        self.action_cooldown = self.reaction_time * 0.8
        return BehaviorTree.SUCCESS

    def do_heavy_kick(self):
        self.stop_moving()
        self.player.handle_event_simulate(SDL_KEYDOWN, SDLK_k)
        self.player.handle_event_simulate(SDL_KEYUP, SDLK_k)
        self.action_cooldown = self.reaction_time * 1.2
        return BehaviorTree.SUCCESS

    def do_anti_air(self):
        self.stop_moving()
        self.player.handle_event_simulate(SDL_KEYDOWN, SDLK_UP)
        self.player.handle_event_simulate(SDL_KEYUP, SDLK_UP)
        self.player.handle_event_simulate(SDL_KEYDOWN, SDLK_k)
        self.player.handle_event_simulate(SDL_KEYUP, SDLK_k)
        self.action_cooldown = self.reaction_time
        return BehaviorTree.SUCCESS

    def do_skill1(self):
        # skill1 커맨드: DOWN -> J -> K
        # input_buffer에 직접 커맨드를 주입하고 마지막 키를 누릅니다.
        self.player.input_buffer = []
        self.player.input_buffer = ['DOWN', 'J']
        self.player.handle_event_simulate(SDL_KEYDOWN, SDLK_k)
        self.action_cooldown = self.reaction_time * 1.5
        return BehaviorTree.SUCCESS

    def do_skill2(self):
        # skill2 커맨드: DOWN -> JUMP -> J
        # input_buffer에 직접 커맨드를 주입하고 마지막 키를 누릅니다.
        self.player.input_buffer = []
        self.player.input_buffer = ['DOWN', 'JUMP']
        self.player.handle_event_simulate(SDL_KEYDOWN, SDLK_j)
        self.action_cooldown = self.reaction_time * 1.5
        return BehaviorTree.SUCCESS

    def do_random_basic_attack(self):
        if random.random() < 0.5:
            return self.do_quick_punch()
        else:
            return self.do_heavy_kick()


    # ==================== Behavior Tree 구성 ====================

    def build_behavior_tree(self):
        # 1. 최우선 순위: 체력이 40 미만일 때의 생존 전략
        survival_strategy = Sequence('🛡️ 생존',
                                     Condition('체력 40 미만?', self.is_self_low_hp),
                                     Selector('후퇴 또는 반격',
                                              # 1-1. 반격 시도: 행동 가능하고 사거리 내에 있으면 반격
                                              Sequence('🚨 위기 시 반격',
                                                       Condition('행동 가능?', self.is_action_ready),
                                                       Condition('공격 사거리?', self.is_target_in_attack_range),
                                                       Action('빠른 펀치', self.do_quick_punch)
                                                       ),
                                              # 1-2. 후퇴: 반격할 수 없으면 후퇴
                                              Action('후퇴', self.move_away_from_target)
                                              )
                                     )

        # 2. 일반 공격 행동 그룹 (체력 40 이상일 때만 실행)
        # 2. 일반 공격 행동 그룹 (체력 40 이상일 때만 실행)
        offensive_behavior = Selector('⚔️ 공격',
                                      Sequence('🔥 피니시!',
                                               Condition('상대 체력 낮음?', self.is_target_low_hp),
                                               Condition('공격 사거리?', self.is_target_in_attack_range),
                                               Selector('필살기 선택', Action('스킬1', self.do_skill1),
                                                        Action('스킬2', self.do_skill2))
                                               ),
                                      Sequence('🥊 근접 전투',
                                               Condition('공격 사거리?', self.is_target_in_attack_range),
                                               Selector('공격 패턴',
                                                        Sequence('✨ 스킬 사용',
                                                                 Condition('스킬 사용?', self.should_use_skill),
                                                                 Selector('스킬 선택', Action('스킬1', self.do_skill1),
                                                                          Action('스킬2', self.do_skill2))
                                                                 ),
                                                        # 펀치와 킥 중 랜덤으로 하나만 실행
                                                        Action('🎲 기본 공격', self.do_random_basic_attack)
                                                        )
                                               )
                                      )

        # 3. 기본 행동: 원거리 접근 또는 정지 (체력 40 이상일 때만 실행)
        default_behavior = Selector('🤔 기본',
                                    Sequence('🚀 원거리', Condition('원거리?', self.is_target_far),
                                             Action('빠른 접근', self.move_toward_target)),
                                    Action('정지', self.stop_moving)
                                    )

        # 최종 루트
        root = Selector('🤖 AI 메인',
                        survival_strategy,  # 1순위: 생존이 최우선
                        Sequence('⚡ 행동',  # 2순위: 생존 문제가 없을 때만 공격/접근
                                 Condition('행동 가능?', self.is_action_ready),
                                 offensive_behavior
                                 ),
                        default_behavior  # 3순위: 그 외 상황 (주로 접근)
                        )

        self.bt = BehaviorTree(root)
