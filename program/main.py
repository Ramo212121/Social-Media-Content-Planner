from datetime import datetime
import os

POSTS_FILE = os.path.join(os.path.dirname(__file__), "posts.txt")
ENGAGEMENT_FILE = os.path.join(os.path.dirname(__file__), "engagement.txt")
PLATFORMS_FILE = os.path.join(os.path.dirname(__file__), "platforms.txt")
REPORT_FILE = os.path.join(os.path.dirname(__file__), "report.txt")


# Load all posts from posts.txt
def load_posts():
    posts = []

    try:
        file = open(POSTS_FILE, "r")

        for line in file:
            data = line.strip().split("|")

            if len(data) == 5:
                post = {
                    "id": data[0].strip(),
                    "platform": data[1].strip(),
                    "caption": data[2].strip(),
                    "date": data[3].strip(),
                    "status": data[4].strip()
                }

                posts.append(post)

        file.close()

    except FileNotFoundError:
        file = open(POSTS_FILE, "w")
        file.close()

    return posts


# Save all posts into posts.txt
def save_posts(posts):
    file = open(POSTS_FILE, "w")

    for post in posts:
        file.write(
            post["id"] + "|" +
            post["platform"] + "|" +
            post["caption"] + "|" +
            post["date"] + "|" +
            post["status"] + "\n"
        )

    file.close()


# Display all posts
def display_posts():
    posts = load_posts()

    if len(posts) == 0:
        print("\nNo posts found.")
        return

    print("\n===== POSTS LIST =====")

    for post in posts:
        print("----------------------------------")
        print("Post ID :", post["id"])
        print("Platform:", post["platform"])
        print("Caption :", post["caption"])
        print("Date    :", post["date"])
        print("Status  :", post["status"])


# Load all platforms from platforms.txt
def load_platforms():
    platforms = []

    try:
        file = open(PLATFORMS_FILE, "r")

        for line in file:
            data = line.strip().split("|")

            if len(data) == 3:
                platform = {
                    "id": data[0].strip(),
                    "name": data[1].strip(),
                    "followers": int(data[2].strip())
                }

                platforms.append(platform)

        file.close()

    except FileNotFoundError:
        file = open(PLATFORMS_FILE, "w")
        file.close()

    return platforms


# Save all platforms into platforms.txt
def save_platforms(platforms):
    file = open(PLATFORMS_FILE, "w")

    for platform in platforms:
        file.write(
            platform["id"] + "|" +
            platform["name"] + "|" +
            str(platform["followers"]) + "\n"
        )

    file.close()


# Works out the next Platform ID by finding the highest existing
# number and adding 1
def get_next_platform_id(platforms):
    max_num = 0

    for platform in platforms:
        num_part = platform["id"].replace("PL", "")

        if num_part.isdigit():
            if int(num_part) > max_num:
                max_num = int(num_part)

    return "PL" + str(max_num + 1)


# Looks up a platform by name. If it already exists, its CANONICAL
# name (the one already stored in platforms.txt) is returned, so that
# posts always use a consistent platform string even if the user
# typed the name with different capitalisation. If it doesn't exist
# yet, the user is asked for a follower count and a new platform
# record is created with an auto-assigned ID, and the name as typed
# is returned.
def register_platform(platform_name):
    platforms = load_platforms()

    for platform in platforms:
        if platform["name"].strip().lower() == platform_name.strip().lower():
            # BUG FIX: return the canonical stored name (not just the
            # ID) so callers can keep platform names consistent across
            # posts.txt, avoiding duplicate/fragmented platform totals
            # in the performance report caused by case differences
            # like "Instagram" vs "instagram"
            return platform["name"]

    followers = input("New platform. Enter Follower Count for " + platform_name + ": ").strip()

    while followers.isdigit() == False:
        print("Follower count must be a number.")
        followers = input("Enter Follower Count for " + platform_name + ": ").strip()

    new_id = get_next_platform_id(platforms)

    new_platform = {
        "id": new_id,
        "name": platform_name,
        "followers": int(followers)
    }

    platforms.append(new_platform)

    save_platforms(platforms)

    print("Platform", platform_name, "registered with ID", new_id)

    return platform_name


# Add a new post
def add_post():
    posts = load_posts()

    post_id = input("Enter Post ID: ").strip().upper()

    if post_id == "":
        print("Post ID cannot be empty.")
        return

    # BUG FIX: '|' is the field delimiter used in posts.txt. If it's
    # allowed inside a field, the line gets split into extra fields on
    # save and the whole record silently disappears the next time the
    # file is loaded (since load_posts() only accepts lines with
    # exactly 5 fields).
    if "|" in post_id:
        print("Post ID cannot contain the '|' character.")
        return

    # Duplicate ID validation
    for post in posts:
        if post["id"].upper() == post_id:
            print("Post ID already exists.")
            return

    platform = input("Enter Platform: ").strip()

    if platform == "":
        print("Platform cannot be empty.")
        return

    if "|" in platform:
        print("Platform cannot contain the '|' character.")
        return

    caption = input("Enter Caption: ").strip()

    if caption == "":
        print("Caption cannot be empty.")
        return

    if "|" in caption:
        print("Caption cannot contain the '|' character.")
        return

    date = input("Enter Date (YYYY-MM-DD): ").strip()

    if date == "":
        print("Date cannot be empty.")
        return

    # Date validation
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    # BUG FIX: platform is now registered only after ALL validation has
    # passed, so platforms.txt never ends up with an orphan platform
    # record for a post that was never actually created. We also use
    # the canonical name it returns so posts.txt stays consistent
    # (e.g. always "Instagram", never a mix of "Instagram"/"instagram")
    platform = register_platform(platform)

    new_post = {
        "id": post_id,
        "platform": platform,
        "caption": caption,
        "date": date,
        "status": "Draft"
    }

    posts.append(new_post)

    save_posts(posts)

    print("Post added successfully.")


# Update the status of a post
def update_post_status():
    posts = load_posts()

    post_id = input("Enter Post ID: ").strip().upper()

    if post_id == "":
        print("Post ID cannot be empty.")
        return

    for post in posts:

        if post["id"].upper() == post_id:

            print("Current Status:", post["status"])

            # BUG FIX: only forward transitions are allowed, as required
            # by the spec (Draft -> Scheduled, Scheduled -> Posted)
            allowed_next_status = {
                "Draft": "Scheduled",
                "Scheduled": "Posted"
            }

            if post["status"] not in allowed_next_status:
                print("This post is already Posted. No further status change is allowed.")
                return

            expected_status = allowed_next_status[post["status"]]

            new_status = input(
                "Enter New Status (" + expected_status + "): "
            ).strip()

            # Status validation
            if new_status != expected_status:
                print("Invalid status. From", post["status"], "you can only move to", expected_status + ".")
                return

            post["status"] = new_status

            save_posts(posts)

            print("Status updated successfully.")
            return

    print("Post not found.")


# Delete a post
def delete_post():
    posts = load_posts()

    post_id = input("Enter Post ID to delete: ").strip().upper()

    if post_id == "":
        print("Post ID cannot be empty.")
        return

    for post in posts:

        if post["id"].upper() == post_id:

            posts.remove(post)

            save_posts(posts)

            print("Post deleted successfully.")
            return

    print("Post not found.")


def post_management_menu():

    while True:

        print("\n===== POST MANAGEMENT =====")
        print("1. Display Posts")
        print("2. Add Post")
        print("3. Update Status")
        print("4. Delete Post")
        print("5. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            display_posts()

        elif choice == "2":
            add_post()

        elif choice == "3":
            update_post_status()

        elif choice == "4":
            delete_post()

        elif choice == "5":
            print("Returning to Main Menu.")
            break

        else:
            print("Invalid Choice.")


# This function reads all engagement data from the file
def load_engagement():
    records = []

    try:
        file = open(ENGAGEMENT_FILE, "r")

        for line in file:
            data = line.strip().split(",")

            if len(data) == 5:
                record = {
                    "post_id": data[0].strip(),
                    "likes": int(data[1].strip()),
                    "comments": int(data[2].strip()),
                    "shares": int(data[3].strip()),
                    "views": int(data[4].strip())
                }
                records.append(record)

        file.close()

    except FileNotFoundError:
        file = open(ENGAGEMENT_FILE, "w")
        file.close()

    return records


# This function adds one new engagement record to the file
def save_engagement(post_id, likes, comments, shares, views):
    file = open(ENGAGEMENT_FILE, "a")

    file.write(post_id + "," + str(likes) + "," + str(comments) + "," + str(shares) + "," + str(views) + "\n")

    file.close()


# This function reads posts.txt so we can check the Post ID and status
def get_posts():
    posts = []

    try:
        file = open(POSTS_FILE, "r")

        for line in file:
            data = line.strip().split("|")

            if len(data) == 5:
                post = {
                    "id": data[0].strip(),
                    "platform": data[1].strip(),
                    "caption": data[2].strip(),
                    "date": data[3].strip(),
                    "status": data[4].strip()
                }
                posts.append(post)

        file.close()

    except FileNotFoundError:
        pass

    return posts


# Menu option 3: user can enter engagement numbers for a Posted post
def record_engagement():
    posts = get_posts()

    post_id = input("Enter Post ID: ").strip().upper()

    if post_id == "":
        print("Post ID cannot be empty.")
        return

    found = False
    post_status = ""

    for post in posts:
        if post["id"].upper() == post_id:
            found = True
            post_status = post["status"]

    if found == False:
        print("Post not found.")
        return

    if post_status != "Posted":
        print("This post is not Posted yet. Current status:", post_status)
        return

    likes = input("Enter Likes: ").strip()
    comments = input("Enter Comments: ").strip()
    shares = input("Enter Shares: ").strip()
    views = input("Enter Views: ").strip()

    # Make sure the user typed numbers, not letters
    if likes.isdigit() == False or comments.isdigit() == False or shares.isdigit() == False or views.isdigit() == False:
        print("Likes, comments, shares and views must be numbers.")
        return

    save_engagement(post_id, likes, comments, shares, views)

    print("Engagement recorded successfully.")


# Menu option 4: show all posts in date order
def display_calendar():
    posts = get_posts()

    if len(posts) == 0:
        print("\nNo posts found.")
        return

    # Skip any post that has a bad date
    good_posts = []

    for post in posts:
        try:
            datetime.strptime(post["date"], "%Y-%m-%d")
            good_posts.append(post)
        except ValueError:
            print("Post", post["id"], "has an invalid date and will be skipped.")

    # Put the posts in date order using bubble sort
    # this checks two posts next to each other and swaps them if
    # they are in the wrong order, it keeps doing this until the
    # whole list is sorted
    n = len(good_posts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if good_posts[j]["date"] > good_posts[j + 1]["date"]:
                temp = good_posts[j]
                good_posts[j] = good_posts[j + 1]
                good_posts[j + 1] = temp

    print("\n===== CONTENT CALENDAR =====")

    for post in good_posts:
        caption = post["caption"]

        if len(caption) > 30:
            caption = caption[:30] + "..."

        print(post["date"], "|", post["platform"], "|", caption, "|", post["status"])


# This function matches each engagement record to its post so we know the platform, then works out the Total Engagement for that post
def build_report_rows():
    posts = get_posts()
    engagement = load_engagement()

    rows = []

    for record in engagement:

        matching_post = None

        for post in posts:
            if post["id"] == record["post_id"]:
                matching_post = post

        if matching_post is None:
            continue

        # Total Engagement = likes + comments + shares
        total_engagement = record["likes"] + record["comments"] + record["shares"]

        row = {
            "post_id": record["post_id"],
            "platform": matching_post["platform"],
            "total_engagement": total_engagement
        }

        rows.append(row)

    return rows


# This function counts how many posts belong to each platform
def get_platform_post_counts():
    posts = get_posts()

    counts = {}

    for post in posts:
        platform = post["platform"]

        if platform in counts:
            counts[platform] += 1
        else:
            counts[platform] = 1

    return counts


# This function finds the post with the highest Total Engagement
def get_best_performing_post(rows):
    best_row = None

    for row in rows:
        if best_row is None or row["total_engagement"] > best_row["total_engagement"]:
            best_row = row

    return best_row


# This function adds up Total Engagement per platform and returns whichever platform has the highest total
def get_most_interactive_platform(rows):
    platform_totals = {}

    for row in rows:
        platform = row["platform"]

        if platform in platform_totals:
            platform_totals[platform] += row["total_engagement"]
        else:
            platform_totals[platform] = row["total_engagement"]

    best_platform = None
    best_total = -1

    for platform in platform_totals:
        if platform_totals[platform] > best_total:
            best_total = platform_totals[platform]
            best_platform = platform

    return best_platform


# Menu option 4: show the performance report on screen
def generate_performance_report():
    rows = build_report_rows()
    platform_counts = get_platform_post_counts()

    print("\n=====================================")
    print("PERFORMANCE REPORT")
    print("=====================================")

    print("Total Posts Per Platform")
    for platform in platform_counts:
        print(platform, ":", platform_counts[platform])

    if len(rows) == 0:
        print("\nNo engagement data recorded yet.")
        return

    best_row = get_best_performing_post(rows)
    most_interactive = get_most_interactive_platform(rows)

    print("\nBest Performing Post")
    print("Post ID :", best_row["post_id"])
    print("Platform:", best_row["platform"])
    print("Total Engagement:", best_row["total_engagement"])

    print("\nMost Interactive Platform")
    print(most_interactive)


# Menu option 5: write the performance report out to report.txt
def export_report_to_file():
    rows = build_report_rows()
    platform_counts = get_platform_post_counts()

    lines = []

    lines.append("PERFORMANCE REPORT")
    lines.append("")

    for platform in platform_counts:
        count = platform_counts[platform]
        label = "post" if count == 1 else "posts"
        lines.append(platform + " : " + str(count) + " " + label)

    if len(rows) == 0:
        lines.append("")
        lines.append("No engagement data recorded yet.")
    else:
        best_row = get_best_performing_post(rows)
        most_interactive = get_most_interactive_platform(rows)

        lines.append("")
        lines.append("Best Post : " + best_row["post_id"])
        lines.append("")
        lines.append("Most Interactive Platform : " + most_interactive)

    file = open(REPORT_FILE, "w")

    for line in lines:
        file.write(line + "\n")

    file.close()

    print("Report exported to", REPORT_FILE)


# Main menu
def menu():

    while True:

        print("\n=====================================")
        print("SOCIAL MEDIA CONTENT PLANNER")
        print("=====================================")
        print("1. Post Management (Add/Update/Display/Delete Posts)")
        print("2. Record Engagement Metrics")
        print("3. Display Content Calendar")
        print("4. Generate Performance Report")
        print("5. Export Report to File")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            post_management_menu()

        elif choice == "2":
            record_engagement()

        elif choice == "3":
            display_calendar()

        elif choice == "4":
            generate_performance_report()

        elif choice == "5":
            export_report_to_file()

        elif choice == "6":
            print("Program Ended.")
            break

        else:
            print("Invalid Choice.")

menu()