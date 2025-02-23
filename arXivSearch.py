import arxiv
import argparse
import os
import webbrowser
import requests

def search_arxiv(query, search_type, result_limit):
    client = arxiv.Client()

    if search_type == "topic":
        search_query = arxiv.Search(query=query, max_results=result_limit)
    elif search_type == "author":
        search_query = arxiv.Search(query=f"au:{query}", max_results=result_limit)
    elif search_type == "subject":
        search_query = arxiv.Search(query=f"cat:{query}", max_results=result_limit)
    else:
        print("Invalid search type.")
        return []

    return list(client.results(search_query))

def display_paginated_results(results, start_index, limit):
    print("\nTop Results:")
    for idx, result in enumerate(results[start_index:start_index + limit], start=start_index + 1):
        print(f"[{idx}] {result.title} ({result.published.year})")
        print(f"    Author(s): {', '.join(author.name for author in result.authors)}")
        print(f"    Abstract: {result.summary[:150]}...")
        print(f"    PDF: {result.pdf_url}\n")
    print(f"Showing results {start_index + 1} to {min(start_index + limit, len(results))} of {len(results)}.\n")

def download_or_open(results, choice, action, filename=None):
    paper = results[choice - 1]
    papers_dir = "./papers"
    os.makedirs(papers_dir, exist_ok=True)

    if action == "download":
        if filename:
            pdf_path = os.path.join(papers_dir, filename)
        else:
            safe_title = paper.title.replace('/', '-').replace(':', '-')
            pdf_path = os.path.join(papers_dir, f"{safe_title}.pdf")
        response = requests.get(paper.pdf_url, stream=True)
        if response.status_code == 200:
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded PDF to {pdf_path}")
        else:
            print(f"Failed to download the PDF. HTTP Status Code: {response.status_code}")
    elif action == "open":
        webbrowser.open(paper.pdf_url)
        print(f"Opening PDF in browser: {paper.pdf_url}")

def handle_user_navigation(results, limit, action, filename=None):
    """Handle pagination and user selection of papers."""
    start_index = 0
    total_results = len(results)

    while True:
        current_page_results = results[start_index:start_index + limit]
        display_paginated_results(results, start_index, limit)

        choice = input("Enter the number of the paper to access, '+' for next page, '-' for previous page, or 0 to exit: ")

        if choice == "0":
            print("Exiting...")
            return 
        elif choice == "+":
            if start_index + limit < total_results:
                start_index += limit
            else:
                print("No more papers to display.")
        elif choice == "-":
            if start_index - limit >= 0:
                start_index -= limit
            else:
                print("You are already on the first page.")
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(results):
                download_or_open(results, choice, action, filename)
                return
            else:
                print("Invalid selection.")
        else:
            print("Invalid input. Please enter a valid number, '+', '-', or '0'.")

def nav_papers():
    papers_dir = "./papers"
    if not os.path.exists(papers_dir):
        print("No papers directory found. Exiting navigation mode.")
        return

    papers = os.listdir(papers_dir)
    if not papers:
        print("No files in the papers directory.")
        return

    while True:
        print("\nPapers in directory:")
        for idx, paper in enumerate(papers, start=1):
            print(f"[{idx}] {paper}")
        print("Options:")
        print("  Enter a number to open a file.")
        print("  Type 'del <number>' to delete a file.")
        print("  Type 'rn <number>' to rename a file.")
        print("  Type 'q' to quit navigation.")

        user_input = input("\nEnter your choice: ").strip()

        if user_input.lower() == "q":
            print("Exiting navigation mode.")
            break

        elif user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(papers):
                file_to_open = os.path.join(papers_dir, papers[choice - 1])
                print(f"Opening: {file_to_open}")
                webbrowser.open(f"file://{os.path.abspath(file_to_open)}")
                break
            else:
                print("Invalid file number.")

        elif user_input.startswith("del "):
            delete_input = user_input.split(" ", 1)[1].strip()
            indices_to_delete = set()

            for part in delete_input.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    indices_to_delete.update(range(start, end + 1))
                else:
                    indices_to_delete.add(int(part))

            indices_to_delete = sorted(indices_to_delete, reverse=True)  
            for idx in indices_to_delete:
                if 1 <= idx <= len(papers):
                    file_to_delete = os.path.join(papers_dir, papers[idx - 1])
                    os.remove(file_to_delete)
                    print(f"Deleted: {papers[idx - 1]}")
                    papers.pop(idx - 1)  # Update list to reflect deletion
                else:
                    print(f"Invalid index: {idx}")

        elif user_input.startswith("rn "):
            try:
                choice = int(user_input.split()[1])
                if 1 <= choice <= len(papers):
                    old_name = papers[choice - 1]
                    old_path = os.path.join(papers_dir, old_name)
                    new_name = input(f"Enter new name for '{old_name}': ").strip()
                    if new_name:
                        new_path = os.path.join(papers_dir, new_name)
                        os.rename(old_path, new_path)
                        print(f"Renamed '{old_name}' to '{new_name}'")
                        papers[choice - 1] = new_name  # Update the list
                    else:
                        print("New name cannot be empty.")
                else:
                    print("Invalid file number.")
            except (ValueError, IndexError):
                print("Invalid input. Use 'rn <number>' to rename a file.")

        else:
            print("Invalid command. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="Search arXiv and access PDFs related to a topic, author, or subject.")
    parser.add_argument("--topic", help="Search for papers by topic or keywords.")
    parser.add_argument("--author", help="Search for papers by a specific author.")
    parser.add_argument("--subject", help="Search for papers by subject area (e.g., 'cond-mat').")
    parser.add_argument("--action", choices=["download", "open"], default="open", help="Action to perform (open in browser or download).")
    parser.add_argument("--limit", help="The display limit of searched papers per page.", default=5, type=int)
    parser.add_argument("--nav_papers", action="store_true", help="Navigate and open downloaded papers in the papers folder.")
    parser.add_argument("--filename", help="Custom filename for the downloaded paper.")
    args = parser.parse_args()

    if args.nav_papers:
        nav_papers()
        return

    if args.topic:
        search_type = "topic"
        query = args.topic
    elif args.author:
        search_type = "author"
        query = args.author
    elif args.subject:
        search_type = "subject"
        query = args.subject
    else:
        print("Please specify one of --topic, --author, or --subject.")
        return

    print(f"Searching arXiv for {search_type}: {query}")
    results = search_arxiv(query, search_type, args.limit * 10)
    if not results:
        print("No results found.")
        return

    handle_user_navigation(results, args.limit, args.action, args.filename)

if __name__ == "__main__":
    os.makedirs("./papers", exist_ok=True)
    main()
