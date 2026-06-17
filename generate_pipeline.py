import os
import requests
import datetime

# 1. Configuration
USERNAME = "Priyanshu-Upadhyay-27"
TOKEN = os.getenv("GH_TOKEN")

# 2. Fetch Contribution Data using GraphQL
def get_contribution_data():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    query = """
    query($userName:String!) {
      user(login: $userName){
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    variables = {"userName": USERNAME}
    response = requests.post('[https://api.github.com/graphql](https://api.github.com/graphql)', json={'query': query, 'variables': variables}, headers=headers)
    return response.json()

# 3. Generate the SVG (The Fun Part!)
def generate_svg(data):
    # This is where you draw the grid, the server, and the animations.
    # We use basic SVG shapes (<rect>, <circle>) and CSS for animation.
    
    total_commits = data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
    
    svg_code = f"""
    <svg width="800" height="300" xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)">
        <style>
            .packet {{
                fill: #00ff88;
                animation: flow 3s infinite linear;
            }}
            @keyframes flow {{
                0% {{ transform: translate(100px, 150px); opacity: 1; }}
                80% {{ transform: translate(600px, 150px); opacity: 1; }}
                100% {{ transform: translate(650px, 150px); opacity: 0; }}
            }}
            .server {{ fill: #1a2332; stroke: #00d4ff; stroke-width: 2; }}
            .text-glow {{ fill: #00ff88; font-family: monospace; font-size: 14px; }}
        </style>

        <!-- Background -->
        <rect width="100%" height="100%" fill="#0d1117" rx="15"/>

        <!-- The MLOps Server Rack -->
        <rect class="server" x="650" y="50" width="100" height="200" rx="10"/>
        <text class="text-glow" x="660" y="80">XGBoost</text>
        <text class="text-glow" x="660" y="120">FastAPI</text>
        
        <!-- The Data Conveyor Belt Line -->
        <line x1="100" y1="150" x2="650" y2="150" stroke="#00d4ff" stroke-width="2" stroke-dasharray="5,5" />

        <!-- Animated Data Packets (Commits) -->
        <circle class="packet" cx="0" cy="0" r="5" />
        <circle class="packet" cx="0" cy="0" r="5" style="animation-delay: 1s;" />
        <circle class="packet" cx="0" cy="0" r="5" style="animation-delay: 2s;" />

        <!-- Total Commits Metric -->
        <text class="text-glow" x="50" y="250">Total Processed: {total_commits}</text>
    </svg>
    """
    
    with open("mlops-pipeline.svg", "w") as f:
        f.write(svg_code)

if __name__ == "__main__":
    data = get_contribution_data()
    generate_svg(data)
    print("MLOps Pipeline SVG Generated Successfully!")
