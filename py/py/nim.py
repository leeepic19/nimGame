import math
import random
import time

class Nim():
    def __init__(self, initial=None, difficulty=None):
        # 用户自定义模式必须传initial
        if difficulty == "custom":
            if initial is None:
                raise ValueError("自定义模式下必须传入initial参数！")
            self.piles = initial.copy()
        elif initial is not None:
            self.piles = initial.copy()
        elif difficulty == "easy":
            self.piles = [2, 4, 5]
        elif difficulty == "hard":
            self.piles = [1, 3, 5, 7, 9]
        else:
            self.piles = [2, 4, 5, 8]
        self.player = 0
        self.winner = None
    @classmethod
    def available_actions(cls, piles):
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions
    @classmethod
    def other_player(cls, player):
        return 0 if player == 1 else 1
    def switch_player(self):
        self.player = Nim.other_player(self.player)
    def move(self, action):
        pile, count = action
        if self.winner is not None:
            raise Exception("游戏已经结束")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("无效的堆编号")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("无效的取物数量")
        self.piles[pile] -= count
        self.switch_player()
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player

class NimAI():
    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
    def update(self, old_state, action, new_state, reward):
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)
    def get_q_value(self, state, action):
        return self.q.get((tuple(state), action), 0)
    def update_q_value(self, state, action, old_q, reward, future_rewards):
        new_q = old_q + self.alpha * (reward + future_rewards - old_q)
        self.q[(tuple(state), action)] = new_q
    def best_future_reward(self, state):
        actions = Nim.available_actions(state)
        if not actions:
            return 0
        best_reward = max(self.get_q_value(state, action) for action in actions)
        return best_reward
    def choose_action(self, state, epsilon=True):
        actions = Nim.available_actions(state)
        if not actions:
            return None
        if epsilon and random.random() < self.epsilon:
            return random.choice(list(actions))
        else:
            best_action = max(actions, key=lambda action: self.get_q_value(state, action))
            return best_action

def train(n, difficulty=None, initial=None):
    player = NimAI()
    for i in range(n):
        if initial is not None:
            game = Nim(initial=initial)
        else:
            game = Nim(difficulty=difficulty)
        print(f"正在进行第 {i + 1} 局训练游戏 训练棋局信息：{game.piles}")
        last = {0: {"state": None, "action": None}, 1: {"state": None, "action": None}}
        while True:
            state = game.piles.copy()
            action = player.choose_action(game.piles)
            last[game.player]["state"] = state
            last[game.player]["action"] = action
            game.move(action)
            new_state = game.piles.copy()
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )
    print("训练完成")
    return player

def play(ai, human_player=None):
    if human_player is None:
        human_player = random.randint(0, 1)
    game = Nim()
    while True:
        print()
        print("当前棋堆:")
        for i, pile in enumerate(game.piles):
            print(f"第{i}堆: {pile} 个")
        print()
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)
        if game.player == human_player:
            print("你的回合")
            while True:
                pile = int(input("请选择要取的堆编号: "))
                count = int(input("请选择要取的数量: "))
                if (pile, count) in available_actions:
                    break
                print("无效的操作，请重试。")
        else:
            print("AI的回合")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI选择从第{pile}堆取走{count}个。")
        game.move((pile, count))
        if game.winner is not None:
            print()
            print("游戏结束")
            winner = "你" if game.winner == human_player else "AI"
            print(f"胜者是：{winner}")
            return