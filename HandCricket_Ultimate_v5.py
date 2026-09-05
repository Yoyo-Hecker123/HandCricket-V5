import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from collections import Counter


SAVE = "hc_v5_stats.json"


class Game:

    # ============================================================
    # TEAM CHALLENGE DEFINITIONS
    # ============================================================]
    # ============================================================
    # TEAM PROGRESSION SYSTEM
    # ============================================================
    
    
    STAR_THRESHOLDS = [
        (0, "🌱 NEW CLUB"),
        (25, "🥉 DEVELOPING CLUB"),
        (60, "🥈 RISING CLUB"),
        (110, "🥇 STRONG CLUB"),
        (175, "💎 ELITE CLUB"),
        (250, "👑 LEGENDARY CLUB")
    ]
    WIN_XP = 5
    CHALLENGE_XP = {
        "New Club": 2,
        "Developing Club": 3,
        "Rising Club": 4,
        "Strong Club": 5,
        "Elite Club": 7,
        "Legendary Club": 10
    }

    STAR_XP = [0, 25, 60, 110, 175, 250]

    TEAM_CHALLENGES = {

        "New Club": [
            ("🏏 First Steps", "Play 1 match"),
            ("🟢 First Victory", "Win 1 match"),
            ("🎯 Getting Started", "Score 25+ runs"),
            ("🔥 First Fifty", "Score 50+ runs"),
            ("⚔️ First Chase", "Successfully chase 50+ runs")
        ],

        "Developing Club": [
            ("💯 Century Club", "Score 100+ runs"),
            ("⚡ Rapid Fire", "Score 75+ runs in 15 balls or fewer"),
            ("🏆 Winning Habit", "Win 3 matches"),
            ("🎯 Chase Specialist", "Successfully chase 100+ runs"),
            ("💥 Big Victory", "Win by 50+ runs")
        ],

        "Rising Club": [
            ("🔥 Run Machine", "Score 150+ runs"),
            ("⚡ Blitzkrieg", "Score 150+ runs in 20 balls or fewer"),
            ("🎯 Master Chaser", "Successfully chase 150+ runs"),
            ("💀 Dominator", "Win by 100+ runs"),
            ("🏆 Winning Side", "Win 5 matches")
        ],

        "Strong Club": [
            ("💥 Double Century", "Score 200+ runs"),
            ("⚡ Perfect Blitz", "Score 200+ runs in 15 balls or fewer"),
            ("🏹 Elite Chaser", "Successfully chase 200+ runs"),
            ("☠️ Ruthless", "Win by 150+ runs"),
            ("🏆 Winning Dynasty", "Win 10 matches")
        ],

        "Elite Club": [
            ("👑 Triple Century", "Score 300+ runs"),
            ("🚀 Impossible Chase", "Successfully chase 250+ runs"),
            ("💀 Absolute Destruction", "Win by 200+ runs"),
            ("🔴 Legendary Assault", "Score 250+ runs on Legendary"),
            ("⚡ Lightning 300", "Score 300+ runs in 30 balls")
        ],

        "Legendary Club": [
            ("🏏 World Record", "Score 498+ runs"),
            ("👑 Legendary Chase", "Successfully chase 300+ runs"),
            ("💀 Ultimate Destroyer", "Win by 250+ runs"),
            ("🔥 Immortal", "Score 400+ runs on Legendary"),
            ("🐐 Hand Cricket GOAT", "Win 25 matches")
        ]
    }

    # ============================================================
    # TEAMS
    # ============================================================

    TEAMS = [
        "Chennai Chargers",
        "Mumbai Mavericks",
        "Delhi Defenders",
        "Kolkata Kings",
        "Bangalore Blasters"
    ]

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, root):

        self.root = root

        self.root.title("🏏 Hand Cricket Legends v5.2")
        self.root.geometry("1100x750")
        self.root.configure(bg="#222222")

        self.team_stats_label = None

        self.load_stats()

        self.menu()

    # ============================================================
    # SAVE SYSTEM
    # ============================================================

    def load_stats(self):

        if os.path.exists(SAVE):

            try:
                with open(SAVE, "r", encoding="utf-8") as f:
                    self.stats = json.load(f)

            except (json.JSONDecodeError, OSError):
                self.stats = {}

        else:
            self.stats = {}

        # ========================================================
        # GLOBAL CAREER DEFAULTS
        # ========================================================

        defaults = {
            "matches": 0,
            "wins": 0,
            "highest": 0,
            "lowest": None,
            "total_runs": 0,
            "highest_sr": 0,
            "biggest_win": 0,
            "biggest_chase": 0
        }

        for key, value in defaults.items():

            if key not in self.stats:
                self.stats[key] = value

        # ========================================================
        # TEAM DATA
        # ========================================================

        if "teams" not in self.stats:
            self.stats["teams"] = {}
        

        for team in self.TEAMS:

            if team not in self.stats["teams"]:

                self.stats["teams"][team] = self.create_empty_team()

            else:

                team_data = self.stats["teams"][team]

                if "matches" not in team_data:
                    team_data["matches"] = 0

                if "wins" not in team_data:
                    team_data["wins"] = 0

                if "highest" not in team_data:
                    team_data["highest"] = 0

                if "total_runs" not in team_data:
                    team_data["total_runs"] = 0
                    
                if "xp" not in team_data:
                    team_data["xp"] = 0

                if "rating" not in team_data:
                    team_data["rating"] = 0.0
                
                if "challenges" not in team_data:
                    team_data["challenges"] = {}

                self.add_missing_challenges(team_data)
                self.update_team_rating(team_data)

        # ========================================================
        # GLOBAL CHALLENGES
        # ========================================================

        if "challenges" not in self.stats:
            self.stats["challenges"] = {}

        global_challenges = [
            "Rookie Challenge",
            "Century Challenge",
            "Run Machine",
            "Destroyer",
            "World Record"
        ]

        for challenge in global_challenges:

            if challenge not in self.stats["challenges"]:
                self.stats["challenges"][challenge] = False

        # ========================================================
        # ONE-TIME TEAM DATA RESET
        #
        # This resets existing team data ONCE.
        #
        # Your global career statistics remain untouched.
        #
        # After this runs, the marker is saved so the teams
        # will NOT be reset every time the game starts.
        # ========================================================

        if not self.stats.get("team_data_reset_v51", False):

            self.reset_team_data_silent()

            self.stats["team_data_reset_v51"] = True

        # ========================================================
        # SAVE
        # ========================================================

        self.save_stats()

    # ============================================================
    # CREATE EMPTY TEAM
    # ============================================================

    def create_empty_team(self):

        challenges = {}

        for tier_challenges in self.TEAM_CHALLENGES.values():

            for challenge_name, requirement in tier_challenges:
                challenges[challenge_name] = False

        return {
            "matches": 0,
            "wins": 0,
            "highest": 0,
            "total_runs": 0,
            "xp": 0,
            "rating": 0.0,
            "challenges": challenges
        }

    # ============================================================
    # ADD MISSING CHALLENGES
    # ============================================================

    def add_missing_challenges(self, team_data):

        if "challenges" not in team_data:
            team_data["challenges"] = {}

        for tier_challenges in self.TEAM_CHALLENGES.values():

            for challenge_name, requirement in tier_challenges:

                if challenge_name not in team_data["challenges"]:
                    team_data["challenges"][challenge_name] = False

    # ============================================================
    # SAVE
    # ============================================================

    def save_stats(self):

        try:

            with open(SAVE, "w", encoding="utf-8") as f:

                json.dump(
                    self.stats,
                    f,
                    indent=4
                )

        except OSError:
            pass

    # ============================================================
    # RESET TEAM DATA
    # ============================================================

    def reset_team_data_silent(self):

        self.stats["teams"] = {}

        for team in self.TEAMS:
            self.stats["teams"][team] = self.create_empty_team()

    # ============================================================
    # MANUAL RESET TEAM DATA
    # ============================================================

    def reset_team_data(self):

        answer = messagebox.askyesno(
            "Reset Team Data",
            "⚠️ RESET ALL TEAM DATA?\n\n"
            "This will reset:\n\n"
            "• Team matches\n"
            "• Team wins\n"
            "• Team scores\n"
            "• Team ratings\n"
            "• Team challenges\n\n"
            "Your overall career statistics will NOT be affected.\n\n"
            "Continue?"
        )

        if not answer:
            return

        self.reset_team_data_silent()

        self.stats["team_data_reset_v51"] = True

        self.save_stats()

        messagebox.showinfo(
            "Team Data Reset",
            "⚔️ TEAM DATA RESET COMPLETE!\n\n"
            "All five teams are now New Clubs.\n"
            "All team challenges are locked again.\n\n"
            "Your Hall of Fame data was preserved."
        )

        self.menu()

    # ============================================================
    # UTILITIES
    # ============================================================

    def clear(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.team_stats_label = None

    # ============================================================
    # MAIN MENU
    # ============================================================

    def menu(self):

        self.clear()

        # ========================================================
        # TITLE
        # ========================================================

        tk.Label(
            self.root,
            text="🏏 HAND CRICKET LEGENDS v5.2",
            font=("Arial", 26, "bold"),
            bg="#222222",
            fg="gold"
        ).pack(pady=20)

        # ========================================================
        # DIFFICULTY
        # ========================================================

        self.diff = ttk.Combobox(
            self.root,
            values=[
                "Easy",
                "Medium",
                "Hard",
                "Legendary"
            ],
            state="readonly"
        )

        self.diff.set("Medium")
        self.diff.pack()

        # ========================================================
        # TEAM SELECT
        # ========================================================

        self.team = ttk.Combobox(
            self.root,
            values=self.TEAMS,
            state="readonly"
        )

        self.team.set("Chennai Chargers")
        self.team.pack(pady=10)

        self.team.bind(
            "<<ComboboxSelected>>",
            self.update_team_stats
        )

        # ========================================================
        # TEAM STATS
        # ========================================================

        self.team_stats_label = tk.Label(
            self.root,
            text="",
            bg="#222222",
            fg="white",
            font=("Arial", 13),
            justify="left"
        )

        self.team_stats_label.pack(pady=10)

        self.update_team_stats()

        # ========================================================
        # START MATCH
        # ========================================================

        tk.Button(
            self.root,
            text="🏏 START MATCH",
            width=20,
            font=("Arial", 14, "bold"),
            command=self.toss_screen
        ).pack(pady=10)

        # ========================================================
        # HALL OF FAME
        # ========================================================

        tk.Button(
            self.root,
            text="🏆 HALL OF FAME",
            width=20,
            font=("Arial", 14, "bold"),
            command=self.hall_of_fame
        ).pack()

        # ========================================================
        # CHALLENGES
        # ========================================================

        tk.Button(
            self.root,
            text="⚔️ CHALLENGES",
            width=20,
            font=("Arial", 14, "bold"),
            command=self.challenge_screen
        ).pack(pady=5)

        # ========================================================
        # RESET TEAM DATA
        # ========================================================

        tk.Button(
            self.root,
            text="🔄 RESET TEAM DATA",
            width=20,
            font=("Arial", 11),
            command=self.reset_team_data
        ).pack(pady=5)

        
    def get_challenge_xp(self, challenge_name):

        for tier_name, challenges in self.TEAM_CHALLENGES.items():

            for name, requirement in challenges:

                if name == challenge_name:

                    return self.CHALLENGE_XP.get(tier_name, 0)

        return 0
    def update_team_rating(self, team):
        xp = team.get("xp", 0)
        if xp >=250:
            rating = 5.0
        elif xp >= 175:
            rating = 4.0
        elif xp >= 110:
            rating = 3.0
        elif xp >= 60:
            rating = 2.0
        elif xp >= 25:
            rating = 1.0
        else:
            rating = round(xp / 25, 2)
        team["rating"] = rating
        return rating

    # ============================================================
    # HALL OF FAME
    # ============================================================



    

    

    # ============================================================
    # MATCH START
    # ============================================================

   

        # ========================================================
        # COMMENTARY
        # ========================================================

    # ============================================================
    # TEAM CAREER DISPLAY
    # ============================================================

    def update_team_stats(self, event=None):

        if not hasattr(self, "team"):
            return

        try:
            team = self.team.get()

        except tk.TclError:
            return

        if not team:
            return

        if "teams" not in self.stats:
            return

        if team not in self.stats["teams"]:
            return

        data = self.stats["teams"][team]

        # XP IS THE SOURCE OF TRUTH
        self.update_team_rating(data)

        xp = data.get("xp", 0)
        rating = data.get("rating", 0.0)

        # ========================================================
        # STAR DISPLAY
        # ========================================================

        full_stars = int(rating)

        half_star = (
            1 if rating - full_stars >= 0.5 else 0
        )

        empty_stars = 5 - full_stars - half_star

        stars = (
            "★" * full_stars
            + ("½" if half_star else "")
            + "☆" * empty_stars
        )

        # ========================================================
        # TEAM STATUS
        # ========================================================

        if rating >= 5.0:
            team_status = "👑 LEGENDARY CLUB"

        elif rating >= 4.0:
            team_status = "💎 ELITE CLUB"

        elif rating >= 3.0:
            team_status = "🥇 STRONG CLUB"

        elif rating >= 2.0:
            team_status = "🥈 RISING CLUB"

        elif rating >= 1.0:
            team_status = "🥉 DEVELOPING CLUB"

        else:
            team_status = "🌱 NEW CLUB"

        # ========================================================
        # WIN RATE
        # ========================================================

        winrate = 0

        if data["matches"]:

            winrate = (
                data["wins"] /
                data["matches"]
            ) * 100

        # ========================================================
        # LABEL
        # ========================================================

        if self.team_stats_label is None:
            return

        try:

            self.team_stats_label.config(

                text=(

                    f"{stars} {rating:.2f} / 5.0\n\n"

                    f"{team_status}\n\n"

                    f"✨ XP          : {xp}\n"

                    f"Matches       : {data['matches']}\n"
                    f"Wins          : {data['wins']}\n"
                    f"Win Rate      : {winrate:.1f}%\n"
                    f"Highest Score : {data['highest']}\n"
                    f"Total Runs    : {data['total_runs']}"
                )
            )

        except tk.TclError:

            pass

    # ============================================================
    # HALL OF FAME
    # ============================================================

    def hall_of_fame(self):

        self.clear()

        # ========================================================
        # TOP BAR
        # ========================================================

        top = tk.Frame(
            self.root,
            bg="#222222"
        )

        top.pack(fill="x")

        tk.Button(
            top,
            text="⬅ Back",
            command=self.menu
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        tk.Label(
            top,
            text="🏆 HALL OF FAME 🏆",
            font=("Arial", 25, "bold"),
            fg="gold",
            bg="#222222"
        ).pack()

        # ========================================================
        # TEXT BOX
        # ========================================================

        box = tk.Text(
            self.root,
            height=25,
            width=80,
            bg="black",
            fg="white",
            font=("Consolas", 12)
        )

        box.pack(pady=10)

        # ========================================================
        # BADGES
        # ========================================================

        badges = self.check_badges()

        unlocked = sum(badges.values())

        # ========================================================
        # WIN RATE
        # ========================================================

        winrate = 0

        if self.stats["matches"]:

            winrate = (
                self.stats["wins"] /
                self.stats["matches"]
            ) * 100

        lowest = self.stats["lowest"]

        if lowest is None:
            lowest = 0

        # ========================================================
        # CAREER RECORDS
        # ========================================================

        header = f"""
══════════════════════════════════════════

              CAREER RECORDS

══════════════════════════════════════════

Matches Played : {self.stats['matches']}
Wins           : {self.stats['wins']}
Win Percentage : {winrate:.1f}%

Highest Score  : {self.stats['highest']}
Lowest Score   : {lowest}

Total Runs     : {self.stats['total_runs']}
Highest SR     : {self.stats['highest_sr']:.2f}

Biggest Win    : {self.stats['biggest_win']}
Biggest Chase  : {self.stats['biggest_chase']}

══════════════════════════════════════════

"""

        box.insert("end", header)

        # ========================================================
        # CAREER LEVEL
        # ========================================================

        current_requirement, current_title = (
            self.get_milestone()
        )

        next_requirement, next_title = (
            self.get_next_milestone()
        )

        matches = self.stats.get("matches", 0)

        milestone_text = f"""
══════════════════════════════════════════

                CAREER LEVEL

══════════════════════════════════════════

Current Title : {current_title}
Matches       : {matches}

"""

        if next_requirement is not None:

            progress_start = current_requirement

            if next_requirement > progress_start:

                progress = (
                    (matches - progress_start)
                    /
                    (next_requirement - progress_start)
                ) * 100

            else:

                progress = 100

            progress = max(
                0,
                min(100, progress)
            )

            remaining = next_requirement - matches

            milestone_text += f"""
Next Milestone : {next_title}
Requirement    : {next_requirement} matches
Remaining      : {remaining} matches
Progress       : {progress:.1f}%

"""

        else:

            milestone_text += """
Next Milestone : MAX LEVEL 👑
Progress       : 100%

"""

        milestone_text += """
══════════════════════════════════════════

"""

        box.insert("end", milestone_text)

        # ========================================================
        # BADGE COLORS
        # ========================================================

        box.tag_config(
            "green",
            foreground="lime"
        )

        box.tag_config(
            "red",
            foreground="red"
        )

        total_badges = len(badges)

        box.insert(
            "end",
            f"\n🏆 BADGE PROGRESS: "
            f"{unlocked}/{total_badges} UNLOCKED\n\n"
        )

        # ========================================================
        # DISPLAY BADGES
        # ========================================================

        for badge, status in badges.items():

            if status:

                box.insert(
                    "end",
                    f"🟢 {badge}\n",
                    "green"
                )

            else:

                box.insert(
                    "end",
                    f"🔴 {badge}\n",
                    "red"
                )

        box.config(state="disabled")

    # ============================================================
    # CAREER MILESTONES
    # ============================================================

    def get_milestone(self):

        matches = self.stats.get("matches", 0)

        milestones = [
            (250, "👑 LEGEND"),
            (100, "💎 SUPERSTAR"),
            (50, "🥇 VETERAN"),
            (25, "🥈 REGULAR"),
            (10, "🥉 CLUB PLAYER"),
            (1, "🏏 ROOKIE")
        ]

        for requirement, title in milestones:

            if matches >= requirement:
                return requirement, title

        return 0, "🌱 BEGINNER"

    # ============================================================

    def get_next_milestone(self):

        matches = self.stats.get("matches", 0)

        milestones = [
            (1, "🏏 ROOKIE"),
            (10, "🥉 CLUB PLAYER"),
            (25, "🥈 REGULAR"),
            (50, "🥇 VETERAN"),
            (100, "💎 SUPERSTAR"),
            (250, "👑 LEGEND")
        ]

        for requirement, title in milestones:

            if matches < requirement:
                return requirement, title

        return None, "👑 MAX LEVEL"

    # ============================================================
    # TOSS
    # ============================================================

    def toss_screen(self):

        self.selected_diff = self.diff.get()
        self.selected_team = self.team.get()

        self.clear()

        tk.Label(
            self.root,
            text="ODD OR EVEN TOSS",
            font=("Arial", 22, "bold"),
            bg="#222222",
            fg="white"
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Odd",
            width=15,
            command=lambda: self.toss("Odd")
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Even",
            width=15,
            command=lambda: self.toss("Even")
        ).pack(pady=5)

    # ============================================================

    def toss(self, choice):

        player = random.randint(1, 10)
        ai = random.randint(1, 10)

        total = player + ai

        won = (
            total % 2 == 0 and choice == "Even"
        ) or (
            total % 2 == 1 and choice == "Odd"
        )

        self.clear()

        tk.Label(
            self.root,
            text=f"You: {player}   AI: {ai}\nTotal: {total}",
            font=("Arial", 16),
            bg="#222222",
            fg="white"
        ).pack(pady=20)

        if won:

            tk.Label(
                self.root,
                text="🔥 You won the toss!",
                bg="#222222",
                fg="lime",
                font=("Arial", 14, "bold")
            ).pack()

            tk.Button(
                self.root,
                text="Bat First",
                command=lambda: self.start(True)
            ).pack(pady=5)

            tk.Button(
                self.root,
                text="Bowl First",
                command=lambda: self.start(False)
            ).pack(pady=5)

        else:

            ai_choice = random.choice([True, False])

            self.start(not ai_choice)

    # ============================================================
    # MATCH START
    # ============================================================

    def start(self, batting):

        self.player_batting = batting
        self.first_batting = batting

        self.innings = 1

        self.player_score = 0
        self.ai_score = 0

        self.player_w = 0
        self.ai_w = 0

        self.player_balls = 0
        self.ai_balls = 0

        self.target = None

        self.history = []

        self.commentary = []

        self.clear()

        # ========================================================
        # SCORE
        # ========================================================

        self.scorelbl = tk.Label(
            self.root,
            font=("Arial", 16, "bold"),
            bg="#222222",
            fg="white"
        )

        self.scorelbl.pack(pady=10)

        # ========================================================
        # PROBABILITY
        # ========================================================

        self.problbl = tk.Label(
            self.root,
            font=("Arial", 12),
            bg="#222222",
            fg="cyan"
        )

        self.problbl.pack()

        # ========================================================
        # BUTTONS
        # ========================================================

        button_frame = tk.Frame(
            self.root,
            bg="#222222"
        )

        button_frame.pack(pady=10)

        for i in range(1, 11):

            tk.Button(
                button_frame,
                text=str(i),
                width=6,
                command=lambda x=i: self.ball(x)
            ).grid(
                row=(i - 1) // 5,
                column=(i - 1) % 5,
                padx=3,
                pady=3
            )

        # ========================================================
        # COMMENTARY
        # ========================================================

        self.feed = tk.Text(
            self.root,
            height=12,
            width=100,
            bg="black",
            fg="lime"
        )

        self.feed.pack()

        # ========================================================
        # SCORECARD
        # ========================================================

        self.card = tk.Text(
            self.root,
            height=15,
            width=100
        )

        self.card.pack(pady=10)

        self.update_screen()

    # ============================================================
    # AI LOGIC
    # ============================================================

    def ai_pick(self):

        difficulty = self.selected_diff

        # ========================================================
        # AI BATTING
        # ========================================================

        if not self.player_batting:

            if difficulty == "Easy":
                return random.randint(1, 10)

            if difficulty == "Medium":

                return random.choice(
                    [3, 4, 5, 6, 7, 8]
                )

            if difficulty == "Hard":

                return random.choice(
                    [4, 5, 6, 7, 8, 9]
                )

            return random.choice(
                [5, 6, 7, 8, 9, 10]
            )

        # ========================================================
        # AI BOWLING
        # ========================================================

        if difficulty == "Easy":
            return random.randint(1, 10)

        if not self.history:
            return random.randint(1, 10)

        common = [
            x
            for x, _
            in Counter(
                self.history
            ).most_common(5)
        ]

        chance = {
            "Medium": 0.30,
            "Hard": 0.55,
            "Legendary": 0.70
        }

        if random.random() < chance[difficulty]:
            return random.choice(common)

        return random.randint(1, 10)

    # ============================================================
    # COMMENTARY
    # ============================================================

    def add_comment(self, msg):

        self.commentary.append(msg)

        self.feed.delete(
            "1.0",
            "end"
        )

        self.feed.insert(
            "end",
            "\n".join(
                self.commentary[-12:]
            )
        )

    # ============================================================
    # BALL ENGINE
    # ============================================================

    def ball(self, num):

        self.history.append(num)

        ai = self.ai_pick()

        # ========================================================
        # PLAYER BATTING
        # ========================================================

        if self.player_batting:

            self.player_balls += 1

            if num == ai:

                self.player_w += 1

                self.add_comment(
                    f"🏏 OUT! You played {num}, AI bowled {ai}"
                )

            else:

                runs = num

                self.player_score += runs

                if runs == 6:
                    msg = "🔥 HUGE SIX!"

                elif runs >= 4:
                    msg = "⚡ Boundary!"

                else:
                    msg = "Nice shot!"

                self.add_comment(
                    f"{msg} +{runs} runs"
                )

            # ====================================================
            # THREE WICKETS
            # ====================================================

            if self.player_w >= 3:

                self.end_innings()

                return

            # ====================================================
            # CHASE COMPLETED
            # ====================================================

            if (
                self.target is not None
                and self.player_score >= self.target
            ):

                self.finish()

                return

        # ========================================================
        # AI BATTING
        # ========================================================

        else:

            self.ai_balls += 1

            if num == ai:

                self.ai_w += 1

                self.add_comment(
                    f"🎯 AI OUT! ({num}={ai})"
                )

            else:

                self.ai_score += ai

                self.add_comment(
                    f"AI scored {ai}"
                )

            # ====================================================
            # THREE WICKETS
            # ====================================================

            if self.ai_w >= 3:

                self.end_innings()

                return

            # ====================================================
            # AI CHASE COMPLETED
            # ====================================================

            if (
                self.target is not None
                and self.ai_score >= self.target
            ):

                self.finish()

                return

        self.update_screen()

    # ============================================================
    # INNINGS MANAGEMENT
    # ============================================================

    def end_innings(self):

        if self.innings == 1:

            self.innings = 2

            if self.player_batting:

                self.target = self.player_score + 1

                self.player_batting = False

                self.add_comment(
                    f"🏏 Innings Break! AI needs {self.target} runs"
                )

            else:

                self.target = self.ai_score + 1

                self.player_batting = True

                self.add_comment(
                    f"🏏 Innings Break! You need {self.target} runs"
                )

            self.update_screen()

        else:

            self.finish()

    # ============================================================
    # MATCH FINISH
    # ============================================================

    def finish(self):

        # ========================================================
        # GENERAL CAREER
        # ========================================================

        self.stats["matches"] += 1

        # ========================================================
        # TEAM
        # ========================================================

        team_data = self.stats["teams"][
            self.selected_team
        ]

        team_data["matches"] += 1

        team_data["total_runs"] += self.player_score

        if self.player_score > team_data["highest"]:

            team_data["highest"] = self.player_score

        # ========================================================
        # TOTAL RUNS
        # ========================================================

        self.stats["total_runs"] += self.player_score

        # ========================================================
        # HIGHEST
        # ========================================================

        if self.player_score > self.stats["highest"]:

            self.stats["highest"] = self.player_score

        # ========================================================
        # LOWEST
        # ========================================================

        if self.stats["lowest"] is None:

            self.stats["lowest"] = self.player_score

        else:

            self.stats["lowest"] = min(
                self.stats["lowest"],
                self.player_score
            )

        # ========================================================
        # STRIKE RATE
        # ========================================================

        sr = (
            self.player_score /
            max(1, self.player_balls)
        ) * 100

        self.stats["highest_sr"] = max(
            self.stats["highest_sr"],
            sr
        )

        # ========================================================
        # WINNER
        # ========================================================

        win = False
        result = ""

        # ========================================================
        # PLAYER BATTED FIRST
        # ========================================================

        if self.first_batting:

            if self.ai_score < self.player_score:

                win = True

                margin = (
                    self.player_score -
                    self.ai_score
                )

                self.stats["biggest_win"] = max(
                    self.stats["biggest_win"],
                    margin
                )

                result = (
                    f"🏆 YOU WON BY {margin} RUNS!"
                )

            else:

                result = "AI WON 😭"

        # ========================================================
        # PLAYER CHASED
        # ========================================================

        else:

            if (
                self.target is not None
                and self.player_score >= self.target
            ):

                win = True

                margin = (
                    3 - self.player_w
                )

                result = (
                    f"🏆 YOU WON BY {margin} WICKETS!"
                )

                self.stats["biggest_chase"] = max(
                    self.stats["biggest_chase"],
                    self.target
                )

            else:

                result = "AI WON 😭"

        # ========================================================
        # WINS
        # ========================================================

        if win:

            self.stats["wins"] += 1

            team_data["wins"] += 1
            team_data["xp"] += self.WIN_XP

        # ========================================================
        # XP-BASED CHALLENGES
        #
        # Rating is NO LONGER increased directly by wins.
        #
        # Challenges award XP.
        # XP determines rating.
        # ========================================================

        new_challenges = self.check_challenges()

        # Make absolutely sure rating reflects the latest XP.

        self.update_team_rating(team_data)

        self.save_stats()

        # ========================================================
        # MATCH RESULT
        # ========================================================

        messagebox.showinfo(

            "MATCH COMPLETE",

            f"{result}\n\n"

            f"🏏 Your Score: "
            f"{self.player_score}/{self.player_w}\n"

            f"🤖 AI Score: "
            f"{self.ai_score}/{self.ai_w}\n\n"

            f"📊 Strike Rate: {sr:.2f}\n"

            f"🏆 Team: {self.selected_team}\n"

            f"✨ Team XP: {team_data['xp']}\n"

            f"⭐ Team Rating: "
            f"{team_data['rating']:.2f}/5.00"
        )

        # ========================================================
        # NEW CHALLENGES
        # ========================================================

        if new_challenges:

            challenge_text = "\n".join(
                f"🏆 {name}  +{xp} XP"
                for name, xp in new_challenges
            )

            messagebox.showinfo(

                "⚔️ CHALLENGES COMPLETED!",

                "🎉 NEW CHALLENGE REWARDS!\n\n"

                f"{challenge_text}\n\n"

                f"✨ Total Team XP: "
                f"{team_data['xp']}\n"

                f"⭐ Team Rating: "
                f"{team_data['rating']:.2f}/5.00"
            )

        self.menu()

    # ============================================================
    # SCREEN UPDATE
    # ============================================================

    def update_screen(self):

        try:

            self.scorelbl.config(

                text=(

                    f"YOU {self.player_score}/{self.player_w}"

                    f"     |     "

                    f"AI {self.ai_score}/{self.ai_w}"
                )
            )

        except tk.TclError:

            return

        # ========================================================
        # WIN PROBABILITY
        # ========================================================

        if self.target is not None:

            if self.player_batting:

                need = (
                    self.target -
                    self.player_score
                )

            else:

                need = (
                    self.target -
                    self.ai_score
                )

            probability = max(
                5,
                min(
                    95,
                    100 - (need * 3)
                )
            )

        else:

            probability = 50

        self.problbl.config(
            text=f"Win Probability: {probability}%"
        )

        # ========================================================
        # PLAYER SR
        # ========================================================

        psr = (
            self.player_score /
            max(1, self.player_balls)
        ) * 100

        self.card.delete(
            "1.0",
            "end"
        )

        # ========================================================
        # AI STRATEGY
        # ========================================================

        if self.selected_diff == "Easy":

            ai_strategy = "🟢 Random Play"

        elif self.selected_diff == "Medium":

            ai_strategy = "🟡 Pattern Reading"

        elif self.selected_diff == "Hard":

            ai_strategy = "🟠 Aggressive Pattern Reading"

        else:

            ai_strategy = "🔴 Elite Pattern Prediction"

        # ========================================================
        # SCORECARD
        # ========================================================

        self.card.insert(

            "end",

            f"""
TEAM: {self.selected_team}

DIFFICULTY: {self.selected_diff}

AI STRATEGY : {ai_strategy}


PLAYER

Runs : {self.player_score}
Balls: {self.player_balls}
Wkts : {self.player_w}
SR   : {psr:.2f}


AI

Runs : {self.ai_score}
Balls: {self.ai_balls}
Wkts : {self.ai_w}


Target:

{self.target if self.target is not None else "-"}
"""
        )

    # ============================================================
    # BADGE SYSTEM
    # ============================================================

    def check_badges(self):

        badges = {

            # ====================================================
            # BRONZE
            # ====================================================

            "🥉 First Match - Play your 1st Game":
                self.stats["matches"] >= 1,

            "🥉 First Win - Get Your First Win":
                self.stats["wins"] >= 1,

            "🥉 Fifty Club - Score a 50":
                self.stats["highest"] >= 50,

            "🥉 Five Matches - Play 5 Matches":
                self.stats["matches"] >= 5,

            "🥉 Survivor - Play 10 Matches":
                self.stats["matches"] >= 10,

            # ====================================================
            # SILVER
            # ====================================================

            "🥈 Century Hero - Score a Century":
                self.stats["highest"] >= 100,

            "🥈 Double Century - Score a Double Century":
                self.stats["highest"] >= 200,

            "🥈 Five Wins - Get 5 Wins":
                self.stats["wins"] >= 5,

            "🥈 Chase Master - Complete a 150+ Chase":
                self.stats["biggest_chase"] >= 150,

            "🥈 Dominator - Get a 100+ Win":
                self.stats["biggest_win"] >= 100,

            # ====================================================
            # GOLD
            # ====================================================

            "🥇 250 Club - Score 250+ Runs":
                self.stats["highest"] >= 250,

            "🥇 300 Club - Score 300+ Runs":
                self.stats["highest"] >= 300,

            "🥇 Strike Monster - Achieve a 500+ Strike Rate":
                self.stats["highest_sr"] >= 500,

            "🥇 Legendary Slayer - Get 15+ Wins":
                self.stats["wins"] >= 15,

            "🥇 Ten Wins - Get 10 Wins":
                self.stats["wins"] >= 10,

            "⭐ Club Builder - Take One Team to 5 Stars":
                any(
                    team["rating"] >= 5.0
                    for team in self.stats["teams"].values()
                ),

            # ====================================================
            # DIAMOND
            # ====================================================

            "💎 400 Club - Score 400+ Runs":
                self.stats["highest"] >= 400,

            "💎 25 Wins - Get 25 Wins":
                self.stats["wins"] >= 25,

            "💎 50 Matches - Play 50 Matches":
                self.stats["matches"] >= 50,

            # ====================================================
            # MYTHIC
            # ====================================================

            "👑 ODI WORLD RECORD - Score 498":
                self.stats["highest"] >= 498,

            "👑 Ultimate Manager - Take All Teams to 5 Stars":
                all(
                    team["rating"] >= 5.0
                    for team in self.stats["teams"].values()
                )
        }

        unlocked = sum(
            badges.values()
        )

        badges[
            "💎 Hall Of Legend - Unlock 15 Badges"
        ] = unlocked >= 15

        return badges

    # ============================================================
    # TEAM CHALLENGE ENGINE
    # ============================================================

    def check_team_challenges(self):

        newly_unlocked = []

        team = self.selected_team

        team_data = self.stats["teams"][team]

        challenges = team_data["challenges"]

        # ========================================================
        # CURRENT MATCH DATA
        # ========================================================

        score = getattr(
            self,
            "player_score",
            0
        )

        balls = getattr(
            self,
            "player_balls",
            0
        )

        difficulty = getattr(
            self,
            "selected_diff",
            ""
        )

        # ========================================================
        # TEAM CAREER DATA
        # ========================================================

        matches = team_data["matches"]

        wins = team_data["wins"]

        highest = team_data["highest"]

        # ========================================================
        # CHALLENGE CONDITIONS
        # ========================================================

        completed = set()

        # ========================================================
        # BASIC SCORE CHALLENGES
        # ========================================================

        if highest >= 25 or score >= 25:

            completed.add(
                "🎯 Getting Started"
            )

        if highest >= 50 or score >= 50:

            completed.add(
                "🔥 First Fifty"
            )

        if highest >= 100 or score >= 100:

            completed.add(
                "💯 Century Club"
            )

        if highest >= 150 or score >= 150:

            completed.add(
                "🔥 Run Machine"
            )

        if highest >= 200 or score >= 200:

            completed.add(
                "💥 Double Century"
            )

        if highest >= 300 or score >= 300:

            completed.add(
                "👑 Triple Century"
            )

        if highest >= 498 or score >= 498:

            completed.add(
                "🏏 World Record"
            )

        # ========================================================
        # WIN CHALLENGES
        # ========================================================

        if wins >= 1:

            completed.add(
                "🟢 First Victory"
            )

        if wins >= 3:

            completed.add(
                "🏆 Winning Habit"
            )

        if wins >= 5:

            completed.add(
                "🏆 Winning Side"
            )

        if wins >= 10:

            completed.add(
                "🏆 Winning Dynasty"
            )

        if wins >= 25:

            completed.add(
                "🐐 Hand Cricket GOAT"
            )

        # ========================================================
        # BALL-BASED CHALLENGES
        #
        # These MUST be achieved in current innings.
        # ========================================================

        if score >= 75 and balls <= 15:

            completed.add(
                "⚡ Rapid Fire"
            )

        if score >= 150 and balls <= 20:

            completed.add(
                "⚡ Blitzkrieg"
            )

        if score >= 200 and balls <= 15:

            completed.add(
                "⚡ Perfect Blitz"
            )

        if score >= 300 and balls <= 30:

            completed.add(
                "⚡ Lightning 300"
            )

        # ========================================================
        # DIFFICULTY CHALLENGES
        # ========================================================

        if difficulty == "Legendary":

            if score >= 250:

                completed.add(
                    "🔴 Legendary Assault"
                )

            if score >= 400:

                completed.add(
                    "🔥 Immortal"
                )

        # ========================================================
        # MATCH COUNT
        # ========================================================

        if matches >= 1:

            completed.add(
                "🏏 First Steps"
            )

        # ========================================================
        # CHASE CHALLENGES
        # ========================================================

        if self.first_batting is False:

            if self.target is not None:

                if score >= self.target:

                    if self.target >= 50:

                        completed.add(
                            "⚔️ First Chase"
                        )

                    if self.target >= 100:

                        completed.add(
                            "🎯 Chase Specialist"
                        )

                    if self.target >= 150:

                        completed.add(
                            "🎯 Master Chaser"
                        )

                    if self.target >= 200:

                        completed.add(
                            "🏹 Elite Chaser"
                        )

                    if self.target >= 250:

                        completed.add(
                            "🚀 Impossible Chase"
                        )

                    if self.target >= 300:

                        completed.add(
                            "👑 Legendary Chase"
                        )

        # ========================================================
        # WIN MARGIN CHALLENGES
        # ========================================================

        if self.first_batting:

            if self.player_score > self.ai_score:

                margin = (
                    self.player_score -
                    self.ai_score
                )

                if margin >= 50:

                    completed.add(
                        "💥 Big Victory"
                    )

                if margin >= 100:

                    completed.add(
                        "💀 Dominator"
                    )

                if margin >= 150:

                    completed.add(
                        "☠️ Ruthless"
                    )

                if margin >= 200:

                    completed.add(
                        "💀 Absolute Destruction"
                    )

                if margin >= 250:

                    completed.add(
                        "💀 Ultimate Destroyer"
                    )

        # ========================================================
        # MARK NEWLY COMPLETED + AWARD XP
        # ========================================================

        for challenge_name in completed:

            if challenge_name in challenges:

                if not challenges[challenge_name]:

                    # Mark challenge complete
                    challenges[challenge_name] = True

                    # Get XP based on challenge tier
                    xp_reward = self.get_challenge_xp(
                        challenge_name
                    )

                    # Award XP
                    team_data["xp"] = (
                        team_data.get("xp", 0)
                        + xp_reward
                    )

                    # Store challenge + XP for popup
                    newly_unlocked.append(
                        (
                            challenge_name,
                            xp_reward
                        )
                    )

        # ========================================================
        # UPDATE RATING FROM XP
        # ========================================================

        self.update_team_rating(team_data)

        # ========================================================
        # SAVE
        # ========================================================

        self.save_stats()

        return newly_unlocked

    # ============================================================
    # CHALLENGE WRAPPER
    # ============================================================

    def check_challenges(self):

        return self.check_team_challenges()

    # ============================================================
    # TEAM CHALLENGE SCREEN
    # ============================================================

    def challenge_screen(self):

        # ========================================================
        # SAVE CURRENT TEAM BEFORE CLEARING
        # ========================================================

        current_team = getattr(
            self,
            "selected_challenge_team",
            None
        )

        if not current_team:

            if hasattr(self, "team"):

                try:

                    current_team = self.team.get()

                except tk.TclError:

                    current_team = None

        if not current_team:

            current_team = "Chennai Chargers"

        self.selected_challenge_team = current_team

        # ========================================================
        # CLEAR SCREEN
        # ========================================================

        self.clear()

        # ========================================================
        # TOP BAR
        # ========================================================

        top = tk.Frame(
            self.root,
            bg="#222222"
        )

        top.pack(
            fill="x"
        )

        tk.Button(
            top,
            text="⬅ Back",
            command=self.menu
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        tk.Label(
            top,
            text="⚔️ TEAM CHALLENGES",
            font=("Arial", 25, "bold"),
            fg="gold",
            bg="#222222"
        ).pack(
            pady=10
        )

        # ========================================================
        # TEAM SELECTOR
        # ========================================================

        selector_frame = tk.Frame(
            self.root,
            bg="#222222"
        )

        selector_frame.pack(
            pady=10
        )

        tk.Label(
            selector_frame,
            text="Select Team:",
            font=("Arial", 13, "bold"),
            bg="#222222",
            fg="white"
        ).pack(
            side="left",
            padx=5
        )

        challenge_team = ttk.Combobox(
            selector_frame,
            values=self.TEAMS,
            state="readonly",
            width=25
        )

        challenge_team.set(
            self.selected_challenge_team
        )

        challenge_team.pack(
            side="left",
            padx=5
        )

        # ========================================================
        # CONTENT FRAME
        # ========================================================

        content = tk.Frame(
            self.root,
            bg="#222222"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # ========================================================
        # SCROLLBAR
        # ========================================================

        scrollbar = tk.Scrollbar(
            content
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        box = tk.Text(
            content,
            width=100,
            height=28,
            bg="black",
            fg="white",
            font=("Consolas", 12),
            yscrollcommand=scrollbar.set
        )

        box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=box.yview
        )

        # ========================================================
        # COLORS
        # ========================================================

        box.tag_config(
            "tier",
            foreground="gold",
            font=("Consolas", 14, "bold")
        )

        box.tag_config(
            "completed",
            foreground="lime"
        )

        box.tag_config(
            "locked",
            foreground="red"
        )

        box.tag_config(
            "requirement",
            foreground="cyan"
        )

        box.tag_config(
            "xp",
            foreground="orange"
        )

        # ========================================================
        # DISPLAY FUNCTION
        # ========================================================

        def display_challenges(team):

            self.selected_challenge_team = team

            box.config(
                state="normal"
            )

            box.delete(
                "1.0",
                "end"
            )

            team_data = self.stats["teams"][team]

            # XP IS THE SOURCE OF TRUTH
            self.update_team_rating(team_data)

            xp = team_data.get("xp", 0)

            rating = team_data.get(
                "rating",
                0.0
            )

            # ====================================================
            # TEAM STATUS
            # ====================================================

            if rating >= 5.0:

                status = "👑 LEGENDARY CLUB"

            elif rating >= 4.0:

                status = "💎 ELITE CLUB"

            elif rating >= 3.0:

                status = "🥇 STRONG CLUB"

            elif rating >= 2.0:

                status = "🥈 RISING CLUB"

            elif rating >= 1.0:

                status = "🥉 DEVELOPING CLUB"

            else:

                status = "🌱 NEW CLUB"

            # ====================================================
            # HEADER
            # ====================================================

            box.insert(
                "end",
                f"\n{team}\n",
                "tier"
            )

            box.insert(
                "end",
                f"{status}\n"
            )

            box.insert(
                "end",
                f"✨ XP: {xp}\n",
                "xp"
            )

            box.insert(
                "end",
                f"⭐ Rating: {rating:.2f} / 5.00\n"
            )

            # ====================================================
            # NEXT RATING TIER
            # ====================================================

            next_tier = None
            next_xp = None

            for threshold, tier_title in self.STAR_THRESHOLDS:

                if xp < threshold:

                    next_xp = threshold
                    next_tier = tier_title

                    break

            if next_xp is not None:

                remaining = next_xp - xp

                box.insert(
                    "end",
                    f"📈 Next Tier: {next_tier}\n"
                    f"🎯 XP Needed: {remaining}\n\n"
                )

            else:

                box.insert(
                    "end",
                    "👑 MAX CLUB RATING REACHED!\n\n"
                )

            box.insert(
                "end",
                f"🏏 Matches: {team_data['matches']}\n"
            )

            box.insert(
                "end",
                f"🏆 Wins: {team_data['wins']}\n"
            )

            box.insert(
                "end",
                f"📊 Highest: {team_data['highest']}\n"
            )

            box.insert(
                "end",
                f"🔥 Total Runs: {team_data['total_runs']}\n\n"
            )

            # ====================================================
            # TIER DISPLAY
            # ====================================================

            tier_names = [
                "New Club",
                "Developing Club",
                "Rising Club",
                "Strong Club",
                "Elite Club",
                "Legendary Club"
            ]

            for tier_name in tier_names:

                tier_xp = self.CHALLENGE_XP.get(
                    tier_name,
                    0
                )

                # Find XP requirement for this tier
                tier_requirement = 0

                for threshold, title in self.STAR_THRESHOLDS:

                    if tier_name.upper() in title:

                        tier_requirement = threshold
                        break

                box.insert(
                    "end",
                    f"\n══════════════════════════════════════════\n"
                    f"        {tier_name}\n"
                    f"══════════════════════════════════════════\n",
                    "tier"
                )

                box.insert(
                    "end",
                    f"✨ Challenge Reward: +{tier_xp} XP each\n"
                )

                tier_challenges = self.TEAM_CHALLENGES[
                    tier_name
                ]

                for challenge_name, requirement in tier_challenges:

                    completed = team_data[
                        "challenges"
                    ].get(
                        challenge_name,
                        False
                    )

                    if completed:

                        box.insert(
                            "end",
                            f"🟢 {challenge_name}\n",
                            "completed"
                        )

                    else:

                        box.insert(
                            "end",
                            f"🔴 {challenge_name}\n",
                            "locked"
                        )

                    box.insert(
                        "end",
                        f"   └─ {requirement}\n",
                        "requirement"
                    )

            box.config(
                state="disabled"
            )

            box.yview_moveto(0)

        # ========================================================
        # TEAM CHANGED
        # ========================================================

        def team_changed(event=None):

            selected = challenge_team.get()

            if selected:

                display_challenges(
                    selected
                )

        challenge_team.bind(
            "<<ComboboxSelected>>",
            team_changed
        )

        # ========================================================
        # INITIAL DISPLAY
        # ========================================================

        display_challenges(
            current_team
        )


# ================================================================
# RUN GAME
# ================================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = Game(root)

    root.mainloop()