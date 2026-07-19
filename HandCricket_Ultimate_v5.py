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
        self.root.title("🏏 Hand Cricket Legends v5")
        self.root.geometry("1100x750")
        self.root.configure(bg="#222222")

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


        # migration for old versions

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


        self.save_stats()



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
            text="🏏 HAND CRICKET LEGENDS v5",
            font=("Arial",26,"bold"),
            bg="#222222",
            fg="gold"
        ).pack(pady=20)



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



        tk.Button(
            self.root,
            text="🏏 START MATCH",
            width=20,
            font=("Arial",14,"bold"),
            command=self.toss_screen
        ).pack(pady=10)



        tk.Button(
            self.root,
            text="🏆 HALL OF FAME",
            width=20,
            font=("Arial",14,"bold"),
            command=self.hall_of_fame
        ).pack()



        tk.Label(
            self.root,
            text=(
                f"\nMatches : {self.stats['matches']}"
                f"\nWins : {self.stats['wins']}"
                f"\nHighest : {self.stats['highest']}"
                f"\nLowest : {self.stats['lowest']}"
            ),
            bg="#222222",
            fg="white",
            font=("Arial",13)
        ).pack(pady=20)



    # ==========================
    # HALL OF FAME
    # ==========================

    def hall_of_fame(self):

        self.clear()

        top = tk.Frame(self.root, bg="#222222")
        top.pack(fill="x")

        tk.Button(
            top,
            text="⬅ Back",
            command=self.menu
        ).pack(side="left", padx=10, pady=10)

        tk.Label(
            top,
            text="🏆 HALL OF FAME 🏆",
            font=("Arial",25,"bold"),
            fg="gold",
            bg="#222222"
        ).pack()

        box = tk.Text(
        self.root,
        height=25,
        width=80,
        bg="black",
        fg="white",
        font=("Consolas",12)
    )

        box.pack(pady=10)

        badges = self.check_badges()
        unlocked = sum(badges.values())

        winrate = 0
        if self.stats["matches"]:
            winrate = (
                self.stats["wins"]
                /
                self.stats["matches"]
            ) * 100

        header = f"""
══════════════════════
       CAREER RECORDS
══════════════════════

Matches Played : {self.stats['matches']}
Wins           : {self.stats['wins']}
Win Percentage : {winrate:.1f}%

Highest Score  : {self.stats['highest']}
Lowest Score   : {self.stats['lowest']}
Total Runs     : {self.stats['total_runs']}

Highest SR     : {self.stats['highest_sr']:.2f}

Biggest Win    : {self.stats['biggest_win']}
Biggest Chase  : {self.stats['biggest_chase']}

══════════════════════
       BADGES {unlocked}/20
══════════════════════

"""

        box.insert("end", header)

        box.tag_config("green", foreground="lime")
        box.tag_config("red", foreground="red")

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
            font=("Arial",22,"bold")
        ).pack(pady=20)


        tk.Button(
            self.root,
            text="Odd",
            width=15,
            command=lambda:self.toss("Odd")
        ).pack(pady=5)


        tk.Button(
            self.root,
            text="Even",
            width=15,
            command=lambda:self.toss("Even")
        ).pack(pady=5)



    def toss(self, choice):

        player = random.randint(1,10)
        ai = random.randint(1,10)

        total = player + ai


        won = (
            total % 2 == 0 and choice=="Even"
        ) or (
            total % 2 == 1 and choice=="Odd"
        )


        self.clear()


        tk.Label(
            self.root,
            text=f"You: {player}   AI: {ai}\nTotal: {total}",
            font=("Arial",16)
        ).pack(pady=20)



        if won:

            tk.Label(
                self.root,
                text="🔥 You won the toss!"
            ).pack()


            tk.Button(
                self.root,
                text="Bat First",
                command=lambda:self.start(True)
            ).pack(pady=5)


            tk.Button(
                self.root,
                text="Bowl First",
                command=lambda:self.start(False)
            ).pack(pady=5)


        else:

            ai_choice = random.choice(
                [True,False]
            )

            self.start(not ai_choice)



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



        self.scorelbl = tk.Label(
            self.root,
            font=("Arial",16,"bold"),
            bg="#222222",
            fg="white"
        )

        self.scorelbl.pack(pady=10)



        self.problbl = tk.Label(
            self.root,
            font=("Arial",12),
            bg="#222222",
            fg="cyan"
        )

        self.problbl.pack()



        button_frame=tk.Frame(
            self.root,
            bg="#222222"
        )

        button_frame.pack(pady=10)



        for i in range(1,11):

            tk.Button(
                button_frame,
                text=str(i),
                width=6,
                command=lambda x=i:self.ball(x)
            ).grid(
                row=(i-1)//5,
                column=(i-1)%5,
                padx=3,
                pady=3
            )



        self.feed=tk.Text(
            self.root,
            height=12,
            width=100,
            bg="black",
            fg="lime"
        )

        self.feed.pack()



        self.card=tk.Text(
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

        difficulty=self.selected_diff



        # AI batting

        if not self.player_batting:

            if difficulty=="Easy":
                return random.randint(1,10)

            if difficulty=="Medium":
                return random.choice(
                    [3,4,5,6,7,8]
                )

            if difficulty=="Hard":
                return random.choice(
                    [4,5,6,7,8,9]
                )


            return random.choice(
                [5,6,7,8,9,10]
            )



        # AI bowling

        if difficulty=="Easy":
            return random.randint(1,10)


        if not self.history:
            return random.randint(1,10)


        common=[
            x for x,_ in
            Counter(self.history).most_common(5)
        ]


        chance={
            "Medium":0.30,
            "Hard":0.55,
            "Legendary":0.70
        }



        if random.random()<chance[difficulty]:

            return random.choice(common)


        return random.randint(1,10)



    # ==========================
    # COMMENTARY
    # ==========================

    def add_comment(self,msg):

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

    def ball(self,num):

        self.history.append(num)

        ai=self.ai_pick()



        # PLAYER BATTING

        if self.player_batting:

            self.player_balls+=1


            if num==ai:

                self.player_w+=1

                self.add_comment(
                    f"🏏 OUT! You played {num}, AI bowled {ai}"
                )


            else:

                runs=num

                self.player_score+=runs


                if runs==6:

                    msg="🔥 HUGE SIX!"

                elif runs>=4:

                    msg="⚡ Boundary!"

                else:

                    msg="Nice shot!"



                self.add_comment(
                    f"{msg} +{runs} runs"
                )



            if self.player_w>=3:

                self.end_innings()

                return



            if self.target and self.player_score>=self.target:

                self.finish()

                return




        # AI BATTING

        else:

            self.ai_balls+=1



            if num==ai:

                self.ai_w+=1

                self.add_comment(
                    f"🎯 AI OUT! ({num}={ai})"
                )



            else:

                self.ai_score+=ai

                self.add_comment(
                    f"AI scored {ai}"
                )



            if self.ai_w>=3:

                self.end_innings()

                return



            if self.target and self.ai_score>=self.target:

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


        else:

            self.finish()



    # ==========================
    # MATCH FINISH
    # ==========================

    def finish(self):

        self.stats["matches"] += 1


        # update runs

        self.stats["total_runs"] += self.player_score



        # highest

        if self.player_score > self.stats["highest"]:

            self.stats["highest"] = self.player_score



        # lowest

        if self.stats["lowest"] is None:

            self.stats["lowest"] = self.player_score

        else:

            self.stats["lowest"] = min(
                self.stats["lowest"],
                self.player_score
            )



        # strike rate

        sr = (
            self.player_score /
            max(1,self.player_balls)
        ) * 100


        self.stats["highest_sr"] = max(
            self.stats["highest_sr"],
            sr
        )



        win=False



        # player batted first

        if self.first_batting:


            if self.ai_score < self.player_score:

                win=True

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



        # player chased

        else:


            if self.player_score >= self.target:

                win=True


                margin = (
                    3-self.player_w
                )


                result = (
                    f"🏆 YOU WON BY {margin} WICKETS!"
                )



                self.stats["biggest_chase"] = max(
                    self.stats["biggest_chase"],
                    self.player_score
                )



            else:

                result="AI WON 😭"



        if win:

            self.stats["wins"] += 1



        self.save_stats()



        messagebox.showinfo(
            "MATCH COMPLETE",
            result
        )


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

            need=self.target-self.ai_score

            probability=max(
                5,
                min(
                    95,
                    100-(need*3)
                )
            )

        else:

            probability=50



        self.problbl.config(
            text=f"Win Probability: {probability}%"
        )



        psr=(
            self.player_score /
            max(1,self.player_balls)
        )*100


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


        badges={

        # Bronze

        "🥉 First Match":
            self.stats["matches"]>=1,


        "🥉 First Win":
            self.stats["wins"]>=1,


        "🥉 Fifty Club":
            self.stats["highest"]>=50,


        "🥉 Survivor":
            self.stats["matches"]>=10,


        "🥉 Five Matches":
            self.stats["matches"]>=5,



        # Silver


        "🥈 Century Hero":
            self.stats["highest"]>=100,


        "🥈 Double Century":
            self.stats["highest"]>=200,


        "🥈 Five Wins":
            self.stats["wins"]>=5,


        "🥈 Chase Master":
            self.stats["biggest_chase"]>=150,


        "🥈 Dominator":
            self.stats["biggest_win"]>=100,



        # Gold


        "🥇 250 Club":
            self.stats["highest"]>=250,


        "🥇 300 Club":
            self.stats["highest"]>=300,


        "🥇 Strike Monster":
            self.stats["highest_sr"]>=500,


        "🥇 Legendary Slayer":
            self.stats["wins"]>=15,


        "🥇 Ten Wins":
            self.stats["wins"]>=10,



        # Diamond


        "💎 400 Club":
            self.stats["highest"]>=400,


        "💎 25 Wins":
            self.stats["wins"]>=25,


        "💎 50 Matches":
            self.stats["matches"]>=50,


        



        # Mythic


        "👑 ODI WORLD RECORD":
            self.stats["highest"]>=498

        }
        unlocked = sum(badges.values())

        badges["💎 Hall Of Legend"] = unlocked >= 15

        return badges



root=tk.Tk()

Game(root)

root.mainloop()