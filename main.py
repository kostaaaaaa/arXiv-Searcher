import arxiv
import argparse
import os
import webbrowser

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

def download_or_open(results, choice, action):
    paper = results[choice - 1]
    if action == "download":
        safe_title = paper.title.replace('/', '-').replace(':', '-')
        pdf_path = f"./papers/{safe_title}.pdf"
        paper.download_pdf(dirpath="./papers")
        print(f"Downloaded PDF to {pdf_path}")
    elif action == "open":
        webbrowser.open(paper.pdf_url)
        print(f"Opening PDF in browser: {paper.pdf_url}")

def handle_user_navigation(results, limit, action):
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
                download_or_open(results, choice, action)
                return
            else:
                print("Invalid selection.")
        else:
            print("Invalid input. Please enter a valid number, '+', '-', or '0'.")

def main():
    parser = argparse.ArgumentParser(description="Search arXiv and access PDFs related to a topic, author, or subject.")
    parser.add_argument("--topic", help="Search for papers by topic or keywords.")
    parser.add_argument("--author", help="Search for papers by a specific author.")
    parser.add_argument("--subject", help="Search for papers by subject area (e.g., 'cond-mat').")
    parser.add_argument("--action", choices=["download", "open"], default="open", help="Action to perform (open in browser or download).")
    parser.add_argument("--limit", help="The display limit of searched papers per page.", default=5, type=int)
    args = parser.parse_args()

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

    handle_user_navigation(results, args.limit, args.action)

if __name__ == "__main__":
    os.makedirs("./papers", exist_ok=True)
    main()