# Setup for everyone

Do these steps once, in order. Most take 5 to 15 minutes; the safety courses take longer. Then go to your subteam's guide: [Mechanical](2-mechanical.md) · [Electrical](3-electrical.md) · [Firmware](4-firmware.md).

## 1. Make your accounts and join Discord

1. Make a free GitHub account at [github.com/signup](https://github.com/signup). Any email works.
2. Join the Electrium Discord: [discord.gg/jggFVza4XR](https://discord.gg/jggFVza4XR).
3. Open the **Bakfiets F26** category. The main channel is **#bakfiets-general**, with four threads:
   - **Bakfiets Mechanical**, **Bakfiets Electrical**, **Bakfiets Firmware**: one per subteam
   - **Github usernames**: post your GitHub username here, and you'll be added to the Electrium-Mobility GitHub org so you can upload your work

The repo is public, so you can download everything before you're added.

## 2. Get the files with GitHub Desktop

Video (optional): [Git, GitHub, & GitHub Desktop for beginners](https://www.youtube.com/watch?v=8Dd7KRpKeaE) (Coder Coder, 22 min).

1. Install [GitHub Desktop](https://desktop.github.com/) and sign in with your GitHub account.
2. Choose **File > Clone repository**, then the **URL** tab.
3. Paste `Electrium-Mobility/Bakfiets-F26`. Leave the local path as it is; by default it's `Documents\GitHub\Bakfiets-F26`.
4. Click **Clone**. It's about 60 MB.
5. Choose **Repository > Show in Explorer**. This folder on your computer is "your clone". Every later step opens files from here, not from the GitHub website.

To get updates later, click **Fetch origin**, then **Pull origin**.

## 3. Safety training

You can do all setup, CAD and code work right away. You need this training before you use tools or touch a battery.

| Training | Needed for | How to get it |
| --- | --- | --- |
| WHMIS 2015 (course code SO2017), about 1 hour, renew every 5 years | Everything in the shop or our room | [LEARN](https://learn.uwaterloo.ca/) > Self Registration. [Safety Office page](https://uwaterloo.ca/safety-office/training/student-safety-orientation-whmis) |
| Engineering Student Machine Shop Orientation | The Engineering Student Shops; you get an access card afterwards | LEARN; score 100% on each module quiz. [Student Shops page](https://uwaterloo.ca/engineering-student-shops/getting-started) |
| Student Design Centre courses: Worker Health and Safety Awareness, and Student Design Centre Safety Requirements | Working in the Sedra Student Design Centre (SDC), where our room is | LEARN. This list comes from the SDC's page for current teams, which needs a UW login |
| Machine training (laser cutter, welding) | Only those machines | Hands-on training from the shop that runs the machine. No onboarding task needs it |

**Battery rules** (from the UW Safety Office [Lithium Cell and Battery Standard](https://uwaterloo.ca/safety-office/laboratory-safety/batteries), plus common practice):

- Never work on a pack alone. Wear safety glasses, take off rings and watches, use insulated tools, and tape over bare terminals.
- Charge and store packs in a fire-resistant LiPo bag, away from anything that burns. Never leave one charging unattended, and don't leave it sitting on the charger.
- Our pack reaches 50.4 V when full, which is over the 50 V line where UW's standard calls for electrical-safety procedures. Use only the matching 12S charger.
- The 2024 pack may have been sitting since 2024 and be over-discharged. Don't charge it until your electrical lead has measured it.
- Never use a swollen or damaged pack. If a pack gets hot, smells or smokes, move everyone away, pull the fire alarm if there's fire, and then tell your electrical lead and the project lead.

## 4. Where the bike is

The bike is in the **Electrium Mobility room in The Bay**, the team work bays in the Sedra Student Design Centre. The SDC gives room access to the members listed on each team's term information form, which the project lead submits. To get on it, post a screenshot of your WHMIS certificate in the **Github usernames** thread, and the project lead adds you.

The whole team meets **Wednesdays, 6 to 7 pm, in the Electrium Mobility room**. Design reviews and team decisions happen there.

## 5. How the team is run

| Role | Person | What they do |
| --- | --- | --- |
| Project lead | Justin Gu | Priorities, decisions that affect more than one subteam (like the motor), purchases, room access |
| Mechanical lead | Being chosen in [issue #17](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/17) | Runs the Bakfiets Mechanical thread, keeps mechanical issues up to date, approves CAD pull requests |
| Electrical lead | Being chosen in [issue #17](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/17) | Same for electrical, and supervises all battery work |
| Firmware lead | Being chosen in [issue #17](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/17) | Same for firmware, and approves code pull requests |

Until the subteam leads are chosen, Justin Gu covers all three roles.

Habits for everyone:

- Post questions in your subteam's thread, where the answer helps the next person too.
- Claim tasks yourself by commenting "I'll take this" on an issue. Nobody needs to assign you.
- Update your issue weekly: what you did, what's next, and anything that's blocking you.
- Anyone can review a pull request; your subteam lead gives the final approval.

## 6. Pick a task and share your work

1. Pick a Stage 2 task from your subteam's table in [ONBOARDING.md](../../ONBOARDING.md). After onboarding, pick from the issues labelled `term project`.
2. Comment "I'll take this". It's yours.
3. In GitHub Desktop, click **Current branch > New branch** and name it after the task, for example `battery-mount-sketch`.
4. Do the work. Save new files in a new folder such as `mechanical/cad-2026/` (create it if it doesn't exist), not inside the 2024 or 2025 folders.
5. Type a one-line summary in the **Summary** box at the bottom left, click **Commit to your-branch**, then **Publish branch**, then **Create Pull Request**. Say what you did and add `Closes #<issue number>`.
6. Post the pull request link in your subteam thread.

If GitHub Desktop says you don't have permission to push and offers to **create a fork**, click **Fork this repository**, then choose **To contribute to the parent project**. A fork is your own copy of the repo on GitHub; your pull request still goes to Bakfiets-F26 as normal. This happens until you've been given write access to the repo.

GitHub's [Hello World guide](https://docs.github.com/en/get-started/start-your-journey/hello-world) walks through branches and pull requests.
