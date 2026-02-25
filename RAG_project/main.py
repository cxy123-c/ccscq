
import os
import sys
import time
import random  # 补充缺失的导入
from openai import OpenAI



import random
import json
from typing import List, Dict, Any
from openai import OpenAI


class BaseAgent:
    """基础Agent类"""
    def __init__(self, name: str, personality: str, client: OpenAI):
        self.name = name
        self.personality = personality
        self.client = client
        self.conversation_history = []
    
    def add_to_history(self, role: str, content: str):
        """添加对话历史"""
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def generate_response(self, user_input: str, context: str = "") -> str:
        """生成回复"""
        import time
        
        system_prompt = f"""你现在扮演{self.name}。{self.personality}
        
当前情境：用户刚刚进入了哆啦A梦的世界，你需要用{self.name}的语气和性格来回应。
请保持角色设定，用温暖友好的方式与用户互动。

{context}
"""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ] + self.conversation_history + [
            {"role": "user", "content": user_input}
        ]
        
        try:
            # 添加思考提示
            print(f"🤔 {self.name}正在思考...", end='', flush=True)
            
            completion = self.client.chat.completions.create(
                model="default",
                temperature=0.7,
                messages=messages,
                stream=False
            )
            
            print(f"\r{'   ' * 10}\r", end='', flush=True)
            
            response = completion.choices[0].message.content
            self.add_to_history("user", user_input)
            self.add_to_history("assistant", response)
            return response
        except Exception as e:
            print(f"\r{'   ' * 10}\r", end='', flush=True)
            return f"[{self.name}]: 抱歉，我现在有点困惑... ({str(e)})"


class DoraemonAgent(BaseAgent):
    """哆啦A梦Agent - 主要的AI助手"""
    def __init__(self, client: OpenAI):
        personality = """你是哆啦A梦，来自22世纪的机器猫。你善良、乐于助人，总是想要帮助朋友们解决问题。
你有一个四次元口袋，里面有各种神奇的道具。你说话时经常会说"诶嘿嘿"、"没问题的"、"交给我吧"等口头禅。
虽然有时候会有点慌张，但总是充满爱心和责任感。你特别怕老鼠，爱吃铜锣烧。"""
        super().__init__("哆啦A梦", personality, client)
        self.tools = [
            "任意门", "竹蜻蜓", "时光机", "缩小灯", "放大灯", "透明斗篷", 
            "记忆面包", "翻译蒟蒻", "如果电话亭", "预知梦枕头", "空气炮",
            "取物袋", "换身镜", "时间包袱巾", "未来日记", "神奇照相机"
        ]
    
    def suggest_tool(self, problem: str) -> str:
        """根据问题建议合适的道具"""
        tool_suggestions = {
            "学习": ["记忆面包", "未来日记", "预知梦枕头"],
            "交通": ["任意门", "竹蜻蜓", "时光机"],
            "沟通": ["翻译蒟蒻", "如果电话亭"],
            "探索": ["透明斗篷", "缩小灯", "放大灯"],
            "回忆": ["时间包袱巾", "神奇照相机"],
            "帮助": ["空气炮", "取物袋", "换身镜"]
        }
        
        for category, tools in tool_suggestions.items():
            if category in problem:
                return f"我觉得{random.choice(tools)}可能会有帮助呢！"
        
        return f"让我从口袋里拿出{random.choice(self.tools)}试试看吧！"


class NobitaAgent(BaseAgent):
    """大雄Agent - 经常需要帮助的朋友"""
    def __init__(self, client: OpenAI):
        personality = """你是野比大雄，一个善良但有些懒惰的小学生。你学习成绩不太好，体育也不行，
经常被胖虎欺负，但你心地善良，有正义感。你总是依赖哆啦A梦的道具，说话时有些胆小但很真诚。
你喜欢静香，害怕胖虎，经常说"哆啦A梦救我"、"真是太好了"等话。"""
        super().__init__("大雄", personality, client)


class ShizukaAgent(BaseAgent):
    """静香Agent - 温柔善良的朋友"""
    def __init__(self, client: OpenAI):
        personality = """你是源静香，一个温柔善良、聪明可爱的女孩子。你总是很关心朋友们，
学习成绩很好，喜欢洗澡和弹钢琴。你说话很温柔有礼貌，经常关心别人的感受，
会说"大家要好好相处呢"、"真是太棒了"等话。你对所有人都很友善。"""
        super().__init__("静香", personality, client)


class GianAgent(BaseAgent):
    """胖虎Agent - 看似粗暴但内心善良"""
    def __init__(self, client: OpenAI):
        personality = """你是刚田武（胖虎），表面上很凶很强势，但内心其实很善良，很保护朋友。
你喜欢唱歌（虽然唱得不好），有时候会欺负大雄，但关键时刻总是会帮助朋友。
你说话比较直接粗暴，但很有义气，经常说"我的东西就是我的，你的东西也是我的"、"跟我来"等话。"""
        super().__init__("胖虎", personality, client)


class SuneoAgent(BaseAgent):
    """小夫Agent - 有些虚荣但也是好朋友"""
    def __init__(self, client: OpenAI):
        personality = """你是骨川小夫，家里很有钱，有些虚荣爱炫耀，但本质上也是个好朋友。
你经常炫耀自己的新玩具或者去过的地方，有时候会和胖虎一起欺负大雄，但也会帮助朋友。
你说话时喜欢炫耀，经常说"我家刚买了"、"真是的"、"看我的"等话。"""
        super().__init__("小夫", personality, client)


class WorldMasterAgent(BaseAgent):
    """世界管理员Agent - 负责场景描述和剧情推进"""
    def __init__(self, client: OpenAI):
        personality = """你是哆啦A梦世界的叙述者和场景管理员。你负责描述当前的环境、
设定场景、推进剧情。你的描述要生动有趣，符合哆啦A梦动漫的风格，充满想象力和温馨感。
你不是某个具体角色，而是整个世界的观察者和叙述者。"""
        super().__init__("场景叙述", personality, client)
    
    def describe_scene(self, location: str = "大雄的房间") -> str:
        """描述当前场景"""
        scenes = {
            "大雄的房间": "你现在在大雄的房间里，榻榻米地板很温暖，书桌上散落着作业本。哆啦A梦的四次元口袋就在旁边，随时可能有神奇的道具出现。",
            "空地": "你来到了孩子们经常玩耍的空地，这里有一个大水管，是大家聚会的地方。天空湛蓝，微风轻拂。",
            "学校": "这里是大雄他们上学的地方，走廊里回荡着孩子们的笑声，充满了青春的活力。",
            "静香家": "静香家很整洁温馨，空气中飘着淡淡的花香，钢琴在角落里静静等待着美妙的音乐。",
            "商店街": "热闹的商店街，各种小店林立，有卖铜锣烧的店铺，哆啦A梦的最爱就在这里。"
        }
        
        return scenes.get(location, f"你现在在{location}，这里充满了哆啦A梦世界特有的温馨和神奇。")


class AgentCoordinator:
    """Agent协调器 - 管理多个Agent的交互"""
    def __init__(self, client: OpenAI):
        self.client = client
        self.doraemon = DoraemonAgent(client)
        self.nobita = NobitaAgent(client)
        self.shizuka = ShizukaAgent(client)
        self.gian = GianAgent(client)
        self.suneo = SuneoAgent(client)
        self.world_master = WorldMasterAgent(client)
        
        self.current_scene = "大雄的房间"
        self.active_agents = [self.doraemon, self.nobita]
        
        self.user_name = "朋友"
        self.user_mood = "好奇"
        
        self.conversation_history = []
        self.max_history_length = 20
        
    def set_scene(self, scene: str):
        """设置当前场景"""
        self.current_scene = scene
        return self.world_master.describe_scene(scene)
    
    def add_to_conversation_history(self, user_input: str, agent_responses: Dict[str, str]):
        """将对话轮次添加到历史记录中"""
        conversation_turn = {
            "user_input": user_input,
            "agent_responses": agent_responses,
            "scene": self.current_scene,
            "active_agents": [agent.name for agent in self.active_agents]
        }
        
        self.conversation_history.append(conversation_turn)
        
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def get_conversation_context(self) -> str:
        """获取对话上下文"""
        if not self.conversation_history:
            return ""
        
        context_lines = ["=== 最近的对话历史 ==="]

        recent_history = self.conversation_history[-5:]
        
        for turn in recent_history:
            context_lines.append(f"用户: {turn['user_input']}")
            for agent_name, response in turn['agent_responses'].items():
                if agent_name != "场景":
                    context_lines.append(f"{agent_name}: {response}")
            context_lines.append("---")
        
        return "\n".join(context_lines)
    
    def add_agent_to_conversation(self, agent_name: str):
        """添加Agent到对话中"""
        agent_map = {
            "大雄": self.nobita,
            "静香": self.shizuka, 
            "胖虎": self.gian,
            "小夫": self.suneo,
            "哆啦A梦": self.doraemon
        }
        
        if agent_name in agent_map and agent_map[agent_name] not in self.active_agents:
            self.active_agents.append(agent_map[agent_name])
            return f"{agent_name}加入了对话！"
        return f"{agent_name}已经在这里了。"
    
    def ensure_multiple_responders(self, user_input: str):
        """确保至少有2-3个角色会回应"""

        if len(self.active_agents) < 2:
            # 根据场景和输入内容智能添加角色
            if self.current_scene == "空地":
                if self.gian not in self.active_agents:
                    self.active_agents.append(self.gian)
                if self.suneo not in self.active_agents:
                    self.active_agents.append(self.suneo)
            elif "静香" in user_input or "女孩" in user_input or "可爱" in user_input:
                if self.shizuka not in self.active_agents:
                    self.active_agents.append(self.shizuka)
            elif "强壮" in user_input or "唱歌" in user_input or "厉害" in user_input:
                if self.gian not in self.active_agents:
                    self.active_agents.append(self.gian)
            else:
                # 随机添加一个角色让对话更丰富
                all_agents = [self.nobita, self.shizuka, self.gian, self.suneo]
                inactive_agents = [agent for agent in all_agents if agent not in self.active_agents]
                if inactive_agents:
                    import random
                    self.active_agents.append(random.choice(inactive_agents))
        
        # 确保哆啦A梦始终在场
        if self.doraemon not in self.active_agents:
            self.active_agents.append(self.doraemon)
    
    def process_user_input(self, user_input: str) -> Dict[str, str]:
        """处理用户输入，协调多个Agent回应"""
        responses = {}
        
        # 确保有多个角色参与对话
        self.ensure_multiple_responders(user_input)
        
        # 场景描述
        if any(keyword in user_input for keyword in ["去", "到", "移动", "走"]):
            if "空地" in user_input:
                responses["场景"] = self.set_scene("空地")
                self.add_agent_to_conversation("胖虎")
                self.add_agent_to_conversation("小夫")
            elif "学校" in user_input:
                responses["场景"] = self.set_scene("学校")
                # 学校场景增加更多角色
                self.add_agent_to_conversation("静香")
                self.add_agent_to_conversation("大雄")
            elif "静香" in user_input and "家" in user_input:
                responses["场景"] = self.set_scene("静香家")
                self.add_agent_to_conversation("静香")
            elif "商店街" in user_input:
                responses["场景"] = self.set_scene("商店街")
                self.add_agent_to_conversation("小夫")  # 小夫喜欢逛街
        
        # 如果提到特定角色，让他们加入对话
        character_mentions = {
            "大雄": "大雄",
            "静香": "静香", 
            "胖虎": "胖虎",
            "小夫": "小夫",
            "哆啦A梦": "哆啦A梦"
        }
        
        for mention, agent_name in character_mentions.items():
            if mention in user_input:
                self.add_agent_to_conversation(agent_name)
        
        # 获取对话历史上下文
        conversation_context = self.get_conversation_context()
        
        # 构建增强的上下文
        context = f"""当前场景：{self.current_scene}
场景描述：{self.world_master.describe_scene(self.current_scene)}
在场角色：{', '.join([agent.name for agent in self.active_agents])}

{conversation_context}

注意：请根据角色性格特点回应，并考虑其他角色可能的反应。让对话自然流畅。"""
        
        # 让活跃的Agent们按照一定顺序回应
        # 优先让被直接提到的角色回应
        response_order = []
        mentioned_agents = []
        
        # 先处理被提到的角色
        for agent in self.active_agents:
            if agent.name in user_input:
                mentioned_agents.append(agent)
                response_order.append(agent)
        
        # 再处理其他活跃角色
        other_agents = [agent for agent in self.active_agents if agent not in mentioned_agents]
        response_order.extend(other_agents)
        
        # 确保至少有2个角色回应
        if len(response_order) < 2:
            # 如果活跃角色不够，临时添加一个
            all_agents = [self.doraemon, self.nobita, self.shizuka, self.gian, self.suneo]
            available_agents = [agent for agent in all_agents if agent not in response_order]
            if available_agents:
                import random
                response_order.append(random.choice(available_agents))
        
        # 生成回应
        import time
        
        # 显示准备对话的提示
        if len(response_order) > 1:
            agent_names = [agent.name for agent in response_order]
            print(f"🎭 {', '.join(agent_names)} 准备回应...", flush=True)
            time.sleep(0.5)
            print()
        
        for i, agent in enumerate(response_order):
            try:
                # 为每个角色提供之前角色的回应作为额外上下文
                if i > 0:
                    previous_responses = []
                    for prev_agent_name, prev_response in responses.items():
                        if prev_agent_name != "场景":
                            previous_responses.append(f"{prev_agent_name}刚刚说: {prev_response}")
                    
                    agent_context = context + "\n\n刚才的回应:\n" + "\n".join(previous_responses)
                    
                    # 在第二个及以后的角色回复前，添加短暂等待
                    print(f"⏳ 等待 {agent.name} 回应...", end='', flush=True)
                    time.sleep(0.8)
                    print(f"\r{'   ' * 15}\r", end='', flush=True)
                else:
                    agent_context = context
                
                response = agent.generate_response(user_input, agent_context)
                responses[agent.name] = response
                
                # 在每个角色回复后稍作停顿
                if i < len(response_order) - 1:  # 不是最后一个角色
                    time.sleep(0.3)
                
            except Exception as e:
                responses[agent.name] = f"[{agent.name}暂时无法回应: {str(e)}]"
        
        # 将本轮对话添加到历史记录
        self.add_to_conversation_history(user_input, responses)
        
        return responses
    
    def get_available_actions(self) -> List[str]:
        """获取可用的动作选项"""
        return [
            "🏠 去大雄的房间",
            "🏞️ 去空地玩耍", 
            "🏫 去学校",
            "🏡 去静香家",
            "🛍️ 去商店街",
            "🎒 请哆啦A梦拿道具",
            "👥 叫朋友们一起玩",
            "❓ 请教问题",
            "�� 说说心里话"
        ] 



def print_with_delay(text: str, delay: float = 0.03):
    """打字效果打印"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_separator():
    """打印分隔线"""
    print("=" * 60)


def print_welcome():
    """打印欢迎信息"""
    welcome_art = """
    ████████╗ ███████╗ ████████╗ ███████╗ ██╗     ██╗
    ██╔═══██║ ██╔═══██║██╔═══██║██╔═══██║██║     ██║
    ██║   ██║ ██║   ██║██║   ██║██║   ██║██║     ██║
    ██║   ██║ ██║   ██║██║   ██║██║   ██║██║     ██║
    ╚██████╔╝ ╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗
     ╚═════╝   ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
    
    🤖✨ 欢迎来到哆啦A梦的神奇世界！✨🤖
    """
    
    print_with_delay(welcome_art, 0.01)
    print_separator()
    print_with_delay("🌟 你即将进入一个充满奇迹和友谊的世界...", 0.05)
    print_with_delay("🎒 哆啦A梦和朋友们正在等待着你的到来！", 0.05)
    print_separator()


def print_scene_transition(scene_name: str):
    """打印场景转换"""
    print_separator()
    print_with_delay(f"📍 正在前往 {scene_name}...", 0.05)
    print("🌈" + "✨" * 20 + "🌈")
    time.sleep(1)


def display_responses(responses: dict):
    """显示Agent们的回应"""
    agent_count = 0
    
    for agent_name, response in responses.items():
        if agent_name == "场景":
            print_with_delay(f"🎬 {response}", 0.02)
            print()
            time.sleep(0.8)  # 场景描述后稍作停顿
        else:
            # 如果不是第一个角色，在回复前添加思考时间
            if agent_count > 0:
                # 不同的思考动画效果
                thinking_animations = [
                    ["💭", "💭.", "💭..", "💭..."],
                    ["🤔", "🤔.", "🤔..", "🤔..."],
                    ["💫", "💫.", "💫..", "💫..."]
                ]
                
                animation = random.choice(thinking_animations)
                
                for frame in animation:
                    print(f"\r{frame}", end='', flush=True)
                    time.sleep(0.3)
                print(f"\r{'   ' * 6}\r", end='', flush=True)  # 清除思考提示
            
            # 为不同角色使用不同的emoji
            emoji_map = {
                "哆啦A梦": "🤖",
                "大雄": "👦", 
                "静香": "👧",
                "胖虎": "💪",
                "小夫": "💰"
            }
            emoji = emoji_map.get(agent_name, "💬")
            
            # 显示角色开始说话的提示
            print_with_delay(f"{emoji} {agent_name}:", 0.03)
            
            # 不同角色的个性化思考时间
            thinking_time = {
                "哆啦A梦": 0.4,  # 科技先进，思考较快
                "静香": 0.3,     # 聪明，反应快
                "小夫": 0.2,     # 机灵，说话快
                "胖虎": 0.5,     # 性格直接，但会稍微思考
                "大雄": 0.6      # 反应较慢，需要更多思考时间
            }.get(agent_name, 0.3)
            
            time.sleep(thinking_time)
            
            # 显示回复内容
            print_with_delay(f"   {response}", 0.025)
            print()
            
            agent_count += 1
            
            # 在角色之间添加适当的间隔
            if agent_count < len([k for k in responses.keys() if k != "场景"]):
                # 随机等待时间，让对话更自然
                wait_time = random.uniform(0.8, 1.5)
                
                # 显示等待下一个角色的提示
                next_agent_index = agent_count
                all_agents = list(responses.keys())
                # 跳过场景键，找到下一个角色
                next_agents = [k for k in all_agents if k != "场景"][agent_count:]
                
                if next_agents:
                    print_with_delay("🔄 其他人也想说话...", 0.02)
                
                time.sleep(wait_time)

def display_current_status(coordinator):
    """显示当前状态信息"""
    print_separator()
    print_with_delay(f"📍 当前场景: {coordinator.current_scene}", 0.02)
    active_names = [agent.name for agent in coordinator.active_agents]
    print_with_delay(f"👥 在场角色: {', '.join(active_names)}", 0.02)
    print_with_delay(f"📚 对话轮次: {len(coordinator.conversation_history)}", 0.02)
    print_separator()


def display_menu(actions: list):
    """显示可用动作菜单"""
    print_separator()
    print_with_delay("🎯 你想要做什么呢？", 0.03)
    print()
    
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
    
    print(f"  0. 💫 自由对话")
    print(f"  h. 📚 查看对话历史")
    print(f"  s. 📊 查看当前状态")
    print(f"  q. 👋 离开哆啦A梦世界")
    print_separator()


def main():
    """主程序"""
    # 初始化OpenAI客户端
    print("正在连接哆啦A梦世界...")
    
    try:
        # 替换为你的真实API配置
        client = OpenAI(
            api_key="f6983782ce03f1372d7aea699a26a3e9f668ed14",  # 替换为你的API Key
            base_url="https://api-fdk9ibp3l0meo7k9.aistudio-app.com/v1"  # 替换为你的接口地址
        )
        
        # 测试连接（可选，注释掉也可以）
        # test_response = client.chat.completions.create(
        #     model="default",
        #     temperature=0.1,
        #     messages=[{"role": "user", "content": "测试连接"}],
        #     max_tokens=10
        # )
        print("✅ 成功连接到哆啦A梦世界！")
        
    except Exception as e:
        print(f"❌ 连接失败：{e}")
        print("请检查你的API配置信息...")
        return
    
    # 初始化Agent协调器
    coordinator = AgentCoordinator(client)
    
    # 显示欢迎信息
    print_welcome()
    
    # 初始化场景
    print_with_delay("🚪 你轻轻推开了一扇神奇的门...", 0.05)
    time.sleep(1)
    
    initial_scene = coordinator.set_scene("大雄的房间")
    print_with_delay(f"🏠 {initial_scene}", 0.03)
    print()
    
    # 哆啦A梦的欢迎
    welcome_responses = coordinator.process_user_input("你好，我是新来的朋友！")
    display_responses(welcome_responses)
    
    # 显示初始状态
    display_current_status(coordinator)
    
    # 主循环
    while True:
        try:
            # 显示可用动作
            actions = coordinator.get_available_actions()
            display_menu(actions)
            
            # 获取用户输入
            user_choice = input("👤 请选择 (输入数字或直接输入你想说的话): ").strip()
            
            if user_choice.lower() == 'q':
                # 退出程序
                print_separator()
                farewell_responses = coordinator.process_user_input("我要离开了，感谢大家！")
                display_responses(farewell_responses)
                print_with_delay("👋 感谢你来到哆啦A梦的世界！希望你度过了愉快的时光！", 0.05)
                print_with_delay("🌟 哆啦A梦世界的大门永远为你敞开！", 0.05)
                break
            
            elif user_choice == '0':
                # 自由对话模式
                print_separator()
                print_with_delay("💬 进入自由对话模式 (输入 'back' 返回菜单)", 0.03)
                print()
                
                while True:
                    user_input = input("👤 你: ").strip()
                    
                    if user_input.lower() == 'back':
                        break
                    
                    if user_input:
                        print()
                        responses = coordinator.process_user_input(user_input)
                        display_responses(responses)
                        # 在自由对话模式中显示简化的状态信息
                        if len(responses) > 1:  # 如果有多个角色回应
                            participating_agents = [name for name in responses.keys() if name != "场景"]
                            print_with_delay(f"👥 参与对话: {', '.join(participating_agents)}", 0.02)
                            print()
            
            elif user_choice.lower() == 'h':
                # 查看对话历史
                print_separator()
                print_with_delay("📚 对话历史回顾", 0.03)
                
                if not coordinator.conversation_history:
                    print_with_delay("暂无对话历史", 0.03)
                else:
                    # 显示最近5轮对话
                    recent_history = coordinator.conversation_history[-5:]
                    for i, turn in enumerate(recent_history, 1):
                        print_with_delay(f"\n=== 第{len(coordinator.conversation_history)-len(recent_history)+i}轮对话 ===", 0.02)
                        print_with_delay(f"📍 场景: {turn['scene']}", 0.02)
                        print_with_delay(f"👤 你: {turn['user_input']}", 0.02)
                        
                        for agent_name, response in turn['agent_responses'].items():
                            if agent_name != "场景":
                                emoji_map = {"哆啦A梦": "🤖", "大雄": "👦", "静香": "👧", "胖虎": "💪", "小夫": "💰"}
                                emoji = emoji_map.get(agent_name, "💬")
                                print_with_delay(f"{emoji} {agent_name}: {response}", 0.02)
                
                input("\n按回车键继续...")
            
            elif user_choice.lower() == 's':
                # 查看当前状态
                display_current_status(coordinator)
                input("按回车键继续...")
            
            elif user_choice.isdigit():
                # 选择预设动作
                choice_index = int(user_choice) - 1
                
                if 0 <= choice_index < len(actions):
                    selected_action = actions[choice_index]
                    print_with_delay(f"✨ 你选择了: {selected_action}", 0.03)
                    
                    # 根据选择执行对应动作
                    action_map = {
                        "🏠 去大雄的房间": "我想去大雄的房间",
                        "🏞️ 去空地玩耍": "我想去空地玩耍", 
                        "🏫 去学校": "我想去学校看看",
                        "🏡 去静香家": "我想去静香家",
                        "🛍️ 去商店街": "我想去商店街逛逛",
                        "🎒 请哆啦A梦拿道具": "哆啦A梦，能给我一个神奇的道具吗？",
                        "👥 叫朋友们一起玩": "大家一起来玩吧！",
                        "❓ 请教问题": "我有个问题想请教大家",
                        "💭 说说心里话": "我想和大家分享一下我的想法"
                    }
                    
                    user_input = action_map.get(selected_action, selected_action)
                    print()
                    responses = coordinator.process_user_input(user_input)
                    display_responses(responses)
                    
                    # 显示参与对话的角色
                    if len(responses) > 1:
                        participating_agents = [name for name in responses.keys() if name != "场景"]
                        print_with_delay(f"👥 本轮参与对话: {', '.join(participating_agents)}", 0.02)
                        print()
                    
                else:
                    print("❌ 无效的选择，请重新输入")
            
            else:
                # 直接处理用户输入
                if user_choice:
                    print()
                    responses = coordinator.process_user_input(user_choice)
                    display_responses(responses)
                    
                    # 显示参与对话的角色
                    if len(responses) > 1:
                        participating_agents = [name for name in responses.keys() if name != "场景"]
                        print_with_delay(f"👥 本轮参与对话: {', '.join(participating_agents)}", 0.02)
                        print()
                else:
                    print("❌ 请输入有效的选择或内容")
            
            # 短暂暂停
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！感谢你来到哆啦A梦的世界！")
            break
        except Exception as e:
            print(f"\n❌ 发生了一个小错误: {e}")
            print("🔧 哆啦A梦正在修复中...")
            time.sleep(2)


if __name__ == "__main__":
    main()