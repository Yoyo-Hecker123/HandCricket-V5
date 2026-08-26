from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from collections import Counter

SAVE = "hc_v5_stats.json"


class Game:

    def __init__(self, root):
        self.root = root
        self.root.title("🏏 Hand Cricket Legends v5.1")
        self.root.geometry("1100x750")
        self.root.configure(bg="#222222")

        self.team_stats_label = None

        self.load_stats()
        self.menu()

    # ==========================
    # SAVE SYSTEM
    # ==========================

    def load_stats(self):

        if os.path.exists(SAVE):
            with open(SAVE, "r") as f:
                self.stats = json.load(f)

        else:
            self.stats = {
                "matches": 0,
                "wins": 0,
                "highest": 0,
                "lowest": None,
                "total_runs": 0,
                "highest_sr": 0,
                "biggest_win": 0,
                "biggest_chase": 0
            }

        # ==========================
        # MIGRATION FOR OLD VERSIONS
        # ==========================

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

        # ==========================
        # TEAM CAREER DATA
        # ==========================

        teams = [
            "Chennai Chargers",
            "Mumbai Mavericks",
            "Delhi Defenders",
            "Kolkata Kings",
            "Bangalore Blasters"
        ]

        if "teams" not in self.stats:
            self.stats["teams"] = {}

        for team in teams:

            if team not in self.stats["teams"]:

                self.stats["teams"][team] = {
                    "matches": 0,
                    "wins": 0,
                    "highest": 0,
                    "total_runs": 0,
                    "rating": 0.0
                }

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

                if "rating" not in team_data:
                    team_data["rating"] = 0.0

        self.save_stats()

    # ==========================
    # SAVE
    # ==========================

    def save_stats(self):

        with open(SAVE, "w") as f:
            json.dump(
                self.stats,
                f,
                indent=4
            )

    # ==========================
    # UTILITIES
    # ==========================

    def clear(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================
    # MAIN MENU
    # ==========================

    def menu(self):

        self.clear()

        tk.Label(
            self.root,
            text="🏏 HAND CRICKET LEGENDS v5.1",
            font=("Arial", 26, "bold"),
            bg="#222222",
            fg="gold"
        ).pack(pady=20)

        # ==========================
        # DIFFICULTY
        # ==========================

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

        # ==========================
        # TEAM SELECT
        # ==========================

        self.team = ttk.Combobox(
            self.root,
            values=[
                "Chennai Chargers",
                "Mumbai Mavericks",
                "Delhi Defenders",
                "Kolkata Kings",
                "Bangalore Blasters"
            ],
            state="readonly"
        )

        self.team.set("Chennai Chargers")
        self.team.pack(pady=10)

        self.team.bind(
            "<<ComboboxSelected>>",
            self.update_team_stats
        )

        # ==========================
        # TEAM STATS LABEL
        # ==========================

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

        # ==========================
        # START MATCH
        # ==========================

        tk.Button(
            self.root,
            text="🏏 START MATCH",
            width=20,
            font=("Arial", 14, "bold"),
            command=self.toss_screen
        ).pack(pady=10)

        # ==========================
        # HALL OF FAME
        # ==========================

        tk.Button(
            self.root,
            text="🏆 HALL OF FAME",
            width=20,
            font=("Arial", 14, "bold"),
            command=self.hall_of_fame
        ).pack()

        # ==========================
        # GENERAL CAREER STATS
        # ==========================

        lowest = self.stats["lowest"]

        if lowest is None:
            lowest = 0

        tk.Label(
            self.root,
            text=(
                f"\nMatches : {self.stats['matches']}"
                f"\nWins : {self.stats['wins']}"
                f"\nHighest : {self.stats['highest']}"
                f"\nLowest : {lowest}"
            ),
            bg="#222222",
            fg="white",
            font=("Arial", 13)
        ).pack(pady=20)

    # ==========================
    # TEAM CAREER DISPLAY
    # ==========================

    def update_team_stats(self, event=None):

        team = self.team.get()

        if not team or "teams" not in self.stats:
            return

        data = self.stats["teams"][team]

        # Make sure old team data has rating
        if "rating" not in data:
            data["rating"] = 0.0

        rating = data["rating"]

        # ==========================
        # STAR DISPLAY
        # ==========================

        full_stars = int(rating)

        half_star = 1 if rating - full_stars >= 0.5 else 0

        empty_stars = 5 - full_stars - half_star

        stars = (
            "★" * full_stars
            + ("½" if half_star else "")
            + "☆" * empty_stars
        )

        # ==========================
        # WIN RATE
        # ==========================

        winrate = 0

        if data["matches"]:
            winrate = (
                data["wins"] /
                data["matches"]
            ) * 100

        # ==========================
        # UPDATE LABEL
        # ==========================

        if self.team_stats_label is None:
            return

        self.team_stats_label.config(
            text=(
                f"{stars} {rating:.1f} / 5.0\n\n"
                f"Matches       : {data['matches']}\n"
                f"Wins          : {data['wins']}\n"
                f"Win Rate      : {winrate:.1f}%\n"
                f"Highest Score : {data['highest']}\n"
                f"Total Runs    : {data['total_runs']}"
            )
        )

    # ==========================
    # HALL OF FAME
    # ==========================

    def hall_of_fame(self):

        self.clear()

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

        box = tk.Text(
            self.root,
            height=25,
            width=80,
            bg="black",
            fg="white",
            font=("Consolas", 12)
        )

        box.pack(pady=10)

        # ==========================
        # BADGES
        # ==========================

        badges = self.check_badges()

        unlocked = sum(badges.values())

        # ==========================
        # WIN RATE
        # ==========================

        winrate = 0

        if self.stats["matches"]:

            winrate = (
                self.stats["wins"]
                /
                self.stats["matches"]
            ) * 100

        lowest = self.stats["lowest"]

        if lowest is None:
            lowest = 0

        # ==========================
        # CAREER RECORDS
        # ==========================

        header = f"""
══════════════════════
       CAREER RECORDS
══════════════════════

Matches Played : {self.stats['matches']}
Wins           : {self.stats['wins']}
Win Percentage : {winrate:.1f}%

Highest Score  : {self.stats['highest']}
Lowest Score   : {lowest}
Total Runs     : {self.stats['total_runs']}

Highest SR     : {self.stats['highest_sr']:.2f}

Biggest Win    : {self.stats['biggest_win']}
Biggest Chase  : {self.stats['biggest_chase']}

══════════════════════

"""

        box.insert(
            "end",
            header
        )

        # ==========================
        # CAREER MILESTONES
        # ==========================

        current_requirement, current_title = (
            self.get_milestone()
        )

        next_requirement, next_title = (
            self.get_next_milestone()
        )

        matches = self.stats.get(
            "matches",
            0
        )

        milestone_text = f"""
══════════════════════════════
        CAREER LEVEL
══════════════════════════════

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

            remaining = (
                next_requirement - matches
            )

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
══════════════════════════════

"""

        box.insert(
            "end",
            milestone_text
        )

        # ==========================
        # BADGE COLORS
        # ==========================

        box.tag_config(
            "green",
            foreground="lime"
        )

        box.tag_config(
            "red",
            foreground="red"
        )

        # ==========================
        # DISPLAY BADGES
        # ==========================

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

        box.config(
            state="disabled"
        )

    # ==========================
    # CAREER MILESTONES
    # ==========================

    def get_milestone(self):

        matches = self.stats.get(
            "matches",
            0
        )

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

    def get_next_milestone(self):

        matches = self.stats.get(
            "matches",
            0
        )

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

    # ==========================
    # TOSS SYSTEM
    # ==========================

    def toss_screen(self):

        self.selected_diff = self.diff.get()
        self.selected_team = self.team.get()

        self.clear()

        tk.Label(
            self.root,
            text="ODD OR EVEN TOSS",
            font=("Arial", 22, "bold")
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
            font=("Arial", 16)
        ).pack(pady=20)

        if won:

            tk.Label(
                self.root,
                text="🔥 You won the toss!"
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

            ai_choice = random.choice(
                [True, False]
            )

            self.start(
                not ai_choice
            )

    # ==========================
    # MATCH START
    # ==========================

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

        # ==========================
        # SCORE LABEL
        # ==========================

        self.scorelbl = tk.Label(
            self.root,
            font=("Arial", 16, "bold"),
            bg="#222222",
            fg="white"
        )

        self.scorelbl.pack(pady=10)

        # ==========================
        # PROBABILITY LABEL
        # ==========================

        self.problbl = tk.Label(
            self.root,
            font=("Arial", 12),
            bg="#222222",
            fg="cyan"
        )

        self.problbl.pack()

        # ==========================
        # BUTTONS
        # ==========================

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

        # ==========================
        # COMMENTARY
        # ==========================

        self.feed = tk.Text(
            self.root,
            height=12,
            width=100,
            bg="black",
            fg="lime"
        )

        self.feed.pack()

        # ==========================
        # SCORECARD
        # ==========================

        self.card = tk.Text(
            self.root,
            height=15,
            width=100
        )

        self.card.pack(pady=10)

        self.update_screen()

    # ==========================
    # AI LOGIC
    # ==========================

    def ai_pick(self):

        difficulty = self.selected_diff

        # ==========================
        # AI BATTING
        # ==========================

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

        # ==========================
        # AI BOWLING
        # ==========================

        if difficulty == "Easy":
            return random.randint(1, 10)

        if not self.history:
            return random.randint(1, 10)

        common = [
            x for x, _
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

    # ==========================
    # COMMENTARY
    # ==========================

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

    # ==========================
    # BALL ENGINE
    # ==========================

    def ball(self, num):

        self.history.append(num)

        ai = self.ai_pick()

        # ==========================
        # PLAYER BATTING
        # ==========================

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

            # Three wickets
            if self.player_w >= 3:

                self.end_innings()
                return

            # Chase completed
            if (
                self.target
                and self.player_score >= self.target
            ):

                self.finish()
                return

        # ==========================
        # AI BATTING
        # ==========================

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

            # Three wickets
            if self.ai_w >= 3:

                self.end_innings()
                return

            # AI chase completed
            if (
                self.target
                and self.ai_score >= self.target
            ):

                self.finish()
                return

        self.update_screen()

    # ==========================
    # INNINGS MANAGEMENT
    # ==========================

    def end_innings(self):

        if self.innings == 1:

            self.innings = 2

            if self.player_batting:

                self.target = (
                    self.player_score + 1
                )

                self.player_batting = False

                self.add_comment(
                    f"🏏 Innings Break! AI needs {self.target} runs"
                )

            else:

                self.target = (
                    self.ai_score + 1
                )

                self.player_batting = True

                self.add_comment(
                    f"🏏 Innings Break! You need {self.target} runs"
                )

        else:

            self.finish()

    # ==========================
    # MATCH FINISH
    # ==========================

    def finish(self):

        # ==========================
        # GENERAL CAREER MATCH
        # ==========================

        self.stats["matches"] += 1

        # ==========================
        # SELECTED TEAM
        # ==========================

        team_data = self.stats["teams"][
            self.selected_team
        ]

        team_data["matches"] += 1

        team_data["total_runs"] += (
            self.player_score
        )

        if self.player_score > team_data["highest"]:

            team_data["highest"] = (
                self.player_score
            )

        # ==========================
        # TEAM RATING PROGRESSION
        # ==========================

        rating = team_data["rating"]

        if rating < 1.0:

            increase = 0.1

        elif rating < 2.0:

            increase = 0.05

        elif rating < 3.0:

            increase = 0.033333

        elif rating < 4.0:

            increase = 0.025

        else:

            increase = 0.02

        team_data["rating"] = min(
            5.0,
            round(
                rating + increase,
                2
            )
        )

        # ==========================
        # TOTAL RUNS
        # ==========================

        self.stats["total_runs"] += (
            self.player_score
        )

        # ==========================
        # HIGHEST SCORE
        # ==========================

        if (
            self.player_score
            > self.stats["highest"]
        ):

            self.stats["highest"] = (
                self.player_score
            )

        # ==========================
        # LOWEST SCORE
        # ==========================

        if self.stats["lowest"] is None:

            self.stats["lowest"] = (
                self.player_score
            )

        else:

            self.stats["lowest"] = min(
                self.stats["lowest"],
                self.player_score
            )

        # ==========================
        # STRIKE RATE
        # ==========================

        sr = (
            self.player_score
            /
            max(1, self.player_balls)
        ) * 100

        self.stats["highest_sr"] = max(
            self.stats["highest_sr"],
            sr
        )

        # ==========================
        # DETERMINE WINNER
        # ==========================

        win = False

        # ==========================
        # PLAYER BATTED FIRST
        # ==========================

        if self.first_batting:

            if self.ai_score < self.player_score:

                win = True

                margin = (
                    self.player_score
                    -
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

        # ==========================
        # PLAYER CHASED
        # ==========================

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
                    self.player_score
                )

            else:

                result = "AI WON 😭"

        # ==========================
        # UPDATE WINS
        # ==========================

        if win:

            self.stats["wins"] += 1

            team_data["wins"] += 1

        # ==========================
        # SAVE
        # ==========================

        self.save_stats()

        # ==========================
        # MATCH MESSAGE
        # ==========================

        messagebox.showinfo(
            "MATCH COMPLETE",
            result
        )

        # ==========================
        # RETURN TO MENU
        # ==========================

        self.menu()

    # ==========================
    # SCREEN UPDATE
    # ==========================

    def update_screen(self):

        self.scorelbl.config(
            text=(
                f"YOU {self.player_score}/{self.player_w}"
                f"     |     "
                f"AI {self.ai_score}/{self.ai_w}"
            )
        )

        if self.target:

            need = (
                self.target
                -
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

        psr = (
            self.player_score
            /
            max(1, self.player_balls)
        ) * 100

        self.card.delete(
            "1.0",
            "end"
        )

        self.card.insert(
            "end",
            f"""
TEAM: {self.selected_team}
DIFFICULTY: {self.selected_diff}


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

{self.target if self.target else "-"}
"""
        )

    # ==========================
    # BADGE SYSTEM
    # ==========================

    def check_badges(self):

        badges = {

            # ==========================
            # BRONZE
            # ==========================

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

            # ==========================
            # SILVER
            # ==========================

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

            # ==========================
            # GOLD
            # ==========================

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

            # ==========================
            # DIAMOND
            # ==========================

            "💎 400 Club - Score 400+ Runs":
                self.stats["highest"] >= 400,

            "💎 25 Wins - Get 25 Wins":
                self.stats["wins"] >= 25,

            "💎 50 Matches - Play 50 Matches":
                self.stats["matches"] >= 50,

            # ==========================
            # MYTHIC
            # ==========================

            "👑 ODI WORLD RECORD - Score 498":
                self.stats["highest"] >= 498
        }

        # ==========================
        # HALL OF LEGEND
        # ==========================

        unlocked = sum(
            badges.values()
        )

        badges[
            "💎 Hall Of Legend - Unlock 15 Badges"
        ] = (
            unlocked >= 15
        )

        return badges


# ==========================
# RUN GAME
# ==========================

if __name__ == "__main__":

    root = tk.Tk()

    game = Game(root)

    root.mainloop()