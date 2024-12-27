# arXiv-Searcher (Terminal)

### Description
A terminal based arXiv search program that allows users to easily access arXiv research papers. Different query options allow users to search based on keywords, topics and authors (hopefully more soon). Without needing to leave the terminal or IDE you are using you can access scholarly articles in a variety of fields. 

### Arguments
- Key Queries
    - `--topic` allows users to search up with keywords in the title or abstract
    - `--author` allows users to search specific authors
    - `--subject` allows users to search specific categories within arXiv.org

- Additional Queries
    - `--action` allows users the choice of either downloading or simply opening a paper, defaults to open
    - `--limit` allows users to change the amount of papers displayed per page on the navigation screen, defaults to 5
    - `--filename` allows the user to specify the filename of the downloaded paper will be saved as in the papers folder
    - `--nav_papers` allows users to view the list of papers downloaded for quick access
        - `<number>` choosing a specific number associated to the paper will allow users to open it in their browser
        - `del <number>` remove specific pdf files from the papers directory of the associated number (ranges and lists of values are able to be deleted as well)
        - `rn <number>` rename specific pdf files from the papers directory of the associated number
        - `q` quit the navigation

- Navigating Queries

### Examples

Example `--topic` query:
```
python .\arXiv_searcher.py --topic "Quantum Computing" 
```
Output:
```
Searching arXiv for topic: Quantum Computing

Top Results:
[1] The Rise of Quantum Internet Computing (2022)
    Author(s): Seng W. Loke
    Abstract: This article highlights quantum Internet computing as referring to
distributed quantum computing over the quantum Internet, analogous to
(classical) I...
    PDF: http://arxiv.org/pdf/2208.00733v1

[2] Unconventional Quantum Computing Devices (2000)
    Author(s): Seth Lloyd
    Abstract: This paper investigates a variety of unconventional quantum computation
devices, including fermionic quantum computers and computers that exploit
nonl...
    PDF: http://arxiv.org/pdf/quant-ph/0003151v1

[3] Geometrical perspective on quantum states and quantum computation (2013)
    Author(s): Zeqian Chen
    Abstract: We interpret quantum computing as a geometric evolution process by
reformulating finite quantum systems via Connes' noncommutative geometry. In
this f...
    PDF: http://arxiv.org/pdf/1311.4939v1

[4] Quantum Computation and Quantum Information (2012)
    Author(s): Yazhen Wang
    Abstract: Quantum computation and quantum information are of great current interest in
computer science, mathematics, physical sciences and engineering. They wi...
    PDF: http://arxiv.org/pdf/1210.0736v1

[5] Google Quantum AI's Quest for Error-Corrected Quantum Computers (2024)
    Author(s): M. AbuGhanem
    Abstract: Quantum computers stand at the forefront of technological innovation,
offering exponential computational speed-ups that challenge classical computing
...
    PDF: http://arxiv.org/pdf/2410.00917v1

Showing results 1 to 5 of 50.

Enter the number of the paper to access, '+' for next page, '-' for previous page, or 0 to exit:
```

If the users desired paper is found on this page, input the number associated to the paper. If not, we can navigate the pages with `+` and `-`. Likewise, we can do the same thing with the other two query types (`--author` and `--subject`) and include the additional query types.

Example `--author` with `--limit`:
```
python .\arXiv_searcher.py --author "Sabine Hossenfelder" --limit 10
```
Output:
```
Searching arXiv for author: Sabine Hossenfelder

Top Results:
[1] The Free Will Function (2012)
    Author(s): Sabine Hossenfelder
    Abstract: It is argued that it is possible to give operational meaning to free will and
the process of making a choice without employing metaphysics....
    PDF: http://arxiv.org/pdf/1202.0720v1

[2] Comment on arXiv:1104.2019, "Relative locality and the soccer ball problem," by Amelino-Camelia et al (2012)
    Author(s): Sabine Hossenfelder
    Abstract: It is explained why the argument in arXiv:1104.2019 does not answer the
question how to describe multi-particle states in models with a deformed
Loren...
    PDF: http://arxiv.org/pdf/1202.4066v1

[3] A No-go theorem for Poincaré-invariant networks (2015)
    Author(s): Sabine Hossenfelder
    Abstract: I explain why there are no Poincar\'e-invariant networks with a locally
finite distribution of nodes and links in Minkowski-spacetime of any dimension...
    PDF: http://arxiv.org/pdf/1504.06070v2

[4] Comment on "No-go theorem for bimetric gravity with positive and negative mass" (2009)
    Author(s): Sabine Hossenfelder
    Abstract: Authors Hohmann and Wohlfarth have put forward a no-go theorem for bimetric
gravity with positive and negative mass in arXiv:0908.3384v1 [gr-qc]. This...
    PDF: http://arxiv.org/pdf/0909.2094v1

[5] Quantum Confusions, Cleared Up (or so I hope) (2023)
    Author(s): Sabine Hossenfelder
    Abstract: I use an instrumental approach to investigate some commonly made claims about
interpretations of quantum mechanics, especially those that pertain ques...
    PDF: http://arxiv.org/pdf/2309.12299v2

[6] Can we measure structures to a precision better than the Planck length? (2012)
    Author(s): Sabine Hossenfelder
    Abstract: It was recently claimed that the Planck length is not a limit to the
precision by which we can measure distances, but that instead it is merely the
Pl...
    PDF: http://arxiv.org/pdf/1205.3636v1

[7] Born's rule from almost nothing (2020)
    Author(s): Sabine Hossenfelder
    Abstract: We here put forward a simple argument for Born's rule based on the
requirement that the probability distribution should not be a function of the
numbe...
    PDF: http://arxiv.org/pdf/2006.14175v2

[8] Antigravitation (2009)
    Author(s): Sabine Hossenfelder
    Abstract: We discuss why there are no negative gravitational sources in General
Relativity and show that it is possible to extend the classical theory such
that...
    PDF: http://arxiv.org/pdf/0909.3456v1

[9] What Black Holes Can Teach Us (2004)
    Author(s): Sabine Hossenfelder
    Abstract: Black holes merge together different field of physics. From General
Relativity over thermodynamics and quantum field theory, they do now also reach
in...
    PDF: http://arxiv.org/pdf/hep-ph/0412265v1

[10] At the Frontier of Knowledge (2010)
    Author(s): Sabine Hossenfelder
    Abstract: At any time, there are areas of science where we are standing at the frontier
of knowledge, and can wonder whether we have reached a fundamental limit...
    PDF: http://arxiv.org/pdf/1001.3538v1

Showing results 1 to 10 of 100.

Enter the number of the paper to access, '+' for next page, '-' for previous page, or 0 to exit:
```

### Requirements
Necessary external packages are `arxiv` and `requests` which can be downloaded with the `requirements.txt` file
```
pip install -r requirements.txt
```
<details>
<summary>Discord Bot Alternative</summary>
<br>
Work in Progress 😢
<br><br>
<b>Current Objectives</b>
<li>
Fully accessible menu 
</li>
<li>
Download feautre in specific text channel
</li>
<li>
Lightweight easy functionality 
</li>
</details>

Have fun! :smiley:
