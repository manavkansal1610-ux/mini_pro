from flask import Flask, render_template_string, abort, jsonify, request
from collections import defaultdict

# Initialize the Flask application
app = Flask(__name__)

# --- COMPLETE MOCK DATABASE (Matching User"s 5 Genres and 5 Books Each) ---
MOCK_POSTS = [
    # Mystery/Thriller
    {
        "id": 1, "title": "Not Quite dead yet ", "author": "Holly Jackson", "date": "2025",
        "category": "Mystery/Thriller",
        "summary": "Not Quite Dead Yet is a propulsive, emotionally charged mystery that uses the ticking clock of impending death to strip away pretense and force its characters—and readers—to confront the truths we most fear.",
        "full_content": "Holly Jackson reimagines the classic whodunit as a race against mortality, blending sharp psychological insight with a deeply human story of regret, love, and the longing for meaning. The novel interrogates the corrosive effects of secrets, the ways families wound and protect each other, and the desperate need to matter before time runs out.Jet's journey is both a gripping investigation and a meditation on what it means to live fully: to choose agency, to seek truth, and to love without guarantees. The final twist—that the killer is the trusted neighbor, acting out of twisted love and resentment—underscores the dangers of unexamined loyalty and the generational cycles of harm. Ultimately, the book's lesson is that life's meaning is found not in grand achievements, but in the small, honest moments of connection, courage, and forgiveness. In her last days, Jet finds what she was searching for all along: not just the answer to her murder, but the freedom to live—and die—on her own terms.",
        "image": "mystery_not_dead.jpg"
    },
    {
        "id": 2, "title": "The Silent Patient", "author": "Alex Michaelides", "date": "2019",
        "category": "Mystery/Thriller",
        "summary": "The Silent Patient is a psychological thriller about artist Alicia Berenson, who is convicted of murdering her husband but has remained completely silent since the crime. Theo Faber, a psychotherapist intrigued by the case, takes a job at the psychiatric facility where Alicia is held in an attempt to get her to talk and unravel the mystery behind the murder.",
        "full_content": " The narrative unfolds through Theo's perspective and Alicia's diary entries, revealing a complex story of trauma, obsession, and deception that blurs the lines between therapist and patient.",
        "image": "mystery_silent_patient.jpg"
    },
    {
        "id": 3, "title": "Gone Girl", "author": "Gillian Flynn", "date": "2012",
        "category": "Mystery/Thriller",
        "summary": "Gone Girl is a psychological thriller about a wife's mysterious disappearance on their fifth anniversary, which makes her husband, Nick, the prime suspect. The story is told from alternating perspectives, revealing the couple's troubled marriage through Nick's present-day narrative and Amy's diary entries from the past.",
        "full_content": " The investigation exposes the dark and complex reality behind their seemingly perfect life, with the mystery ultimately leading to a shocking revelation about Amy's true intentions. ",
        "image": "mystery_gone_girl.jpg"
    },
    {
        "id": 4, "title": "The Girl in Room 105", "author": "Chetan Bhagat", "date": "2018",
        "category": "Mystery/Thriller",
        "summary": "The Girl in Room 105 is about Keshav, a man still in love with his ex-girlfriend Zara, who finds her murdered after she texts him to meet her in her hostel room on her birthday.",
        "full_content": " Keshav, with the help of his friend Saurabh, launches an investigation to uncover the truth behind her death, delving into themes of love, obsession, and societal issues. The book explores the dark side of obsession and leads Keshav on a journey filled with mystery, twists, and eventually the discovery that Zara's fiancé, Raghu, was the killer.",
        "image": "mystery_girl_room_105.jpg"
    },
    {
        "id": 5, "title": "The Secret of Secrets", "author": "Dan Brown", "date": "2025",
        "category": "Mystery/Thriller",
        "summary": "The Secret of Secrets is a 2025 Robert Langdon novel by Dan Brown where the symbology professor races to find his partner, Katherine Solomon, who vanishes in Prague after a brutal murder. Solomon, a noetic scientist, was on the verge of a discovery that challenges the nature of consciousness, attracting the attention of a dangerous conspiracy.",
        "full_content": " Langdon must navigate Prague's ancient and modern mysteries, facing off against a mystic assassin and a powerful organization in a thrilling race against time, as described on Dan Brown Official Website.",
        "image": "mystery_da_vinci.jpg"
    },
    
    # Romance
    {
        "id": 6, "title": "Wonder", "author": "R.J. Palacio", "date": "2012",
        "category": "Romance",
        "summary": "Wonder is a novel by R.J. Palacio about ten-year-old August Auggie Pullman, a boy born with a significant facial deformity who attends mainstream school for the first time in the fifth grade.",
        "full_content": " The story, which is told from multiple perspectives, follows Auggie as he navigates friendships, bullying, and the challenges of being different, while inspiring those around him to embrace kindness, acceptance, and courage",
        "image": "romance_wonder.jpg"
    },
    {
        "id": 7, "title": "Anne of Green Gables", "author": "L. M. Montgomery", "date": "1908",
        "category": "Romance",
        "summary": "Anne of Green Gables is a classic novel by Lucy Maud Montgomery about an imaginative orphan, Anne Shirley, who is mistakenly sent to live with elderly siblings, Matthew and Marilla Cuthbert, on their Prince Edward Island farm.",
        "full_content": " The story follows Anne's journey as she grows up, forms deep friendships, and navigates life's challenges with her unique spirit, eventually winning over the Cuthberts and finding her home.",
        "image": "romance_spanish.jpg"
    },
    {
        "id": 8, "title": "The Fault in Our Stars", "author": "John Green", "date": "2012",
        "category": "Romance",
        "summary": "The Fault in Our Stars is a love story about two teenagers with cancer, Hazel Grace Lancaster and Augustus Waters, who meet at a support group. They bond over their shared experiences, including a love for the novel An Imperial Affliction, and fall in love.",
        "full_content": " Their relationship is marked by their witty dialogues, intellectual conversations, and their desire for a normal teenage life despite their illnesses. A major plot point involves their trip to Amsterdam to meet the author of An Imperial Affliction, which leads to the discovery of Augustus's cancer's return.",
        "image": "romance_royal.jpg"
    },
    {
        "id": 9, "title": "Everything everything", "author": "Nicola Yoon", "date": "2015",
        "category": "Romance",
        "summary": "Everything, Everything is about Maddy Whittier, an 18-year-old who has lived her entire life inside her home due to a severe immune deficiency (SCID), which makes her allergic to the world. Her life of isolation is disrupted when a new family moves in next door, and she begins a relationship with the boy next door, Olly, first online and then through secret, risky meetings.",
        "full_content": " The story follows their forbidden romance as Maddy yearns to experience life outside her sterile environment.",
        "image": "romance_everything.jpg"
    },
    {
        "id": 10, "title": "Flipped", "author": "Wendelin Van Draanen", "date": "2001",
        "category": "Romance",
        "summary": "Flipped is a coming-of-age story about Juli Baker and Bryce Loski, told from both of their alternating perspectives. The novel (and film adaptation) follows their relationship over several years, starting from second grade, as their initial feelings for each other ,flip and evolve.",
        "full_content": " Juli is instantly smitten, while Bryce tries to avoid her, but eventually, their perspectives shift, and Bryce begins to see Juli differently, just as she starts to realize he isn't the perfect boy she once thought.",
        "image": "romance_flipped.jpg"
    },
    
    # Science
    {
        "id": 11, "title": "The Time Machine", "author": "H.G. Wells", "date": "1895",
        "category": "Science Fiction",
        "summary": "The Time Machine by H.G. Wells is a novel about a Victorian scientist who builds a machine to travel through time and visits the year 802,701.",
        "full_content": " There, he discovers humanity has diverged into two species: the childlike, surface-dwelling Eloi (descendants of the wealthy) and the monstrous, underground-dwelling Morlocks (descendants of the working class). The story is framed by the scientist recounting his adventures to skeptical friends, and he ultimately journeys even further into the future and is never seen again.",
        "image": "science_time_machine.jpg"
    },
    {
        "id": 12, "title": "Frankenstein", "author": "Mary Shelley", "date": "1818",
        "category": "Science Fiction",
        "summary": " Frankenstein is a gothic novel by Mary Shelley about Victor Frankenstein, a scientist who creates a sentient creature in an attempt to play God, but then abandons it in horror. The creature, shunned for its appearance, learns from humans but becomes vengeful after its creator's rejection.",
        "full_content": " This leads the creature to murder Victor's loved ones, resulting in a tragic cycle of revenge that culminates in Victor's death in the Arctic and the creature's vow of suicide.",
        "image": "science_cosmos.jpg"
    },
    {
        "id": 13, "title": "1984", "author": "George Orwell", "date": "1949",
        "category": "Science Fiction",
        "summary": "George Orwell's 1984 is a dystopian novel about Winston Smith, who lives under the oppressive rule of the Party and its leader, Big Brother, in the totalitarian superstate of Oceania.",
        "full_content": " Winston begins a secret affair with Julia to rebel against the Party's control over free thought, history, and individuality. They are eventually caught and taken to the Ministry of Love, where Winston is systematically tortured by O'Brien until he fully renounces his beliefs and loves Big Brother.",
        "image": "science_hawking.jpg"
    },
    {
        "id": 14, "title": "Dune", "author": "Frank Herbert", "date": "1965",
        "category": "Science Fiction",
        "summary": "Dune is a science fiction novel by Frank Herbert about a young nobleman, Paul Atreides, who becomes a messianic leader on the desert planet Arrakis. His family, House Atreides, is forced to take control of Arrakis, the universe's only source of the valuable spice, melange, a substance vital for interstellar travel and consciousness-expanding abilities.",
        "full_content": " After his family is betrayed by rivals House Harkonnen and the Padishah Emperor, Paul and his mother Jessica escape into the desert, where they are taken in by the native Fremen. The story follows Paul as he embraces his destiny, leads the Fremen, and seeks revenge, ultimately leading to a conflict that will change the universe.",
        "image": "science_dune.jpg"
    },
    {
        "id": 15, "title": "The Martian", "author": "Andy Weir", "date": "2011",
        "category": "Science Fiction",
        "summary": "The Martian by Andy Weir is a science fiction novel about astronaut Mark Watney, who is presumed dead and left behind on Mars after a storm. The story follows his resourceful struggle to survive alone on the planet by using his knowledge as a botanist and mechanical engineer to grow food, produce water, and ultimately find a way to signal Earth and await rescue.",
        "full_content": " The novel is driven by Watney's ingenuity, humor, and resilience as he overcomes numerous scientific and engineering challenges to stay alive.",
        "image": "science_hela.jpg"
    },
    

    # Historical Events (Historical Fiction)
    {
        "id": 16, "title": "The Book Thief", "author": "Markus Zusak", "date": "2005",
        "category": "Historical Fiction",
        "summary": "The Book Thief is a historical fiction novel by Markus Zusak set in Nazi Germany during World War II and narrated by Death.",
        "full_content": " It follows the story of a young girl named Liesel Meminger, who is sent to live with foster parents and finds solace and a connection to others through stealing and reading books. The story highlights her relationship with her foster father, Hans, her best friend Rudy Steiner, and a Jewish man named Max Vandenberg whom her family hides in their basement. The narrative culminates in a devastating air raid that kills Hans, Rosa, and Rudy, but Liesel ultimately survives and is reunited with Max after the war.",
        "image": "history_book_thief.jpg"
    },
  
    {
        "id": 17, "title": "The Diary of a Young Girl", "author": "Anne Frank", "date": "1959",
        "category": "Historical Fiction",
        "summary": "The Diary of a Young Girl is the diary of Anne Frank, a Jewish teenage girl who went into hiding in Amsterdam during World War 2. This diary describes her life in hiding for 2 years including her relationships, fears, and coming-of-age experiences.",
        "full_content": " After their hiding place was discovered, the family was arrested and sent to concentration camps where Anne did not survive. Her father, Otto, was the sole survivor and later published her diary, which became a world-famous testament to hope and the human spirit during the Holocaust.",
        "image": "history_unbroken.jpg"
    },
    {
        "id": 18, "title": "Schindler's List", "author": "Thomas Keneally", "date": "1982",
        "category": "Historical Fiction",
        "summary": "Schindler's List is a novel by Thomas Keneally based on the historical figure Oskar Schindler. Initially a member of the Nazi party who sought to profit from World War 2, Schindler evolves into a protector of over 1,100 Polish Jews.",
        "full_content": " He uses his factory to employ them, transforming it into a safe haven where he risks his life and fortune to save them from the Holocaust's death camps. The plot culminates with Schindler compiling a list of his Jewish employees, saving them from extermination before the war ends and the Soviet army liberates the area.",
        "image": "history_pillars.jpg"
    },
      {
        "id": 19, "title": "The Nightingale", "author": "Kristin Hannah", "date": "2015",
        "category": "Historical Fiction",
        "summary": "The Nightingale is a 2015 historical novel by Kristin Hannah about two sisters in German-occupied France during World War II, following their vastly different paths of survival and resistance.",
        "full_content": " The story contrasts the passive resistance of the older sister, Vianne, who is forced to house a German soldier and protect her family, with the active heroism of the younger sister, Isabelle, who joins the French Resistance to help downed Allied airmen escape.",
        "image": "history_nightingale.jpg"
    },
    {
        "id": 20, "title": "The Tattooist of Auschwitz", "author": "Heather Morris", "date": "2018",
        "category": "Historical Fiction",
        "summary": "The Tattooist of Auschwitz is a novel by Heather Morris based on the true story of Lale Sokolov, a Slovakian Jew who was imprisoned at the Auschwitz concentration camp in 1942. While working as the camp's tattooist, he falls in love with Gita Furman, a fellow prisoner he is tasked with tattooing.",
        "full_content": " The book recounts their experiences surviving the horrors of Auschwitz, their eventual reunion after being separated, and their post-war life together in Melbourne, Australia.",
        "image": "history_tattooist.jpg"
    },
   

    # Self-help
    {
        "id": 21, "title": "The 7 Habits of Highly Effective People", "author": "Stephen R. Covey", "date": "1989",
        "category": "Self-help",
        "summary": "The 7 Habits of Highly Effective People by Stephen R. Covey outlines a character-based approach to personal and professional effectiveness, moving from dependence to independence and then to interdependence.",
        "full_content": "The 7 Habits of Highly Effective People by Stephen R. Covey outlines a character-based approach to personal and professional effectiveness, moving from dependence to independence and then to interdependence.",
        "image": "selfhelp_7habits.jpg"
    },
    {
        "id": 22, "title": "Atomic Habits", "author": "James Clear", "date": "2018",
        "category": "Self-help",
        "summary": "Atomic Habits by James Clear is a book that explains how tiny, consistent changes can lead to remarkable results by focusing on small habits that build over time.",
        "full_content": " The core idea is to create a system for improvement rather than focusing on long-term goals, using the 'Four Laws of Behavior Change' to make good habits easy and bad habits difficult: make it obvious, make it attractive, make it easy, and make it satisfying.",
        "image": "selfhelp_atomic.jpg"
    },
   
    {
        "id": 23, "title": "The Power of Now", "author": "Eckhart Tolle", "date": "1997",
        "category": "Self-help",
        "summary": "Eckhart Tolle's 'The Power of Now' is a spiritual guide that argues most human suffering comes from identifying with the mind, and true peace is found by living in the present moment, not dwelling on the past or future.",
        "full_content": " The book encourages readers to observe their thoughts without judgment, accept the now, and recognize their true being beyond the ego. Key concepts include detaching from the 'pain-body' of accumulated past suffering and embracing acceptance as a path to inner peace",
        "image": "selfhelp_daring.jpg"
    },
    {
        "id": 24, "title": "Think and Grow Rich", "author": "Napoleon Hill", "date": "1937",
        "category": "Self-help",
        "summary": "Napoleon Hill, then a young special investigator for a nationally known business magazine, was sent to interview Andrew Carnegie. During that interview, Carnegie slyly dropped a hint of a certain master power he used—a magic law of the human mind, a little-known psychological principle—that was amazing in its power.",
        "full_content": " Carnegie suggested to Hill that upon that principle he could build the philosophy of all personal success—whether it be measured in terms of money, power, position, prestige, influence, or the accumulation of wealth. That part of the interview never made it into Hill’s magazine, but it did launch the young author on a research journey that lasted twenty years. Think and Grow Rich is the result of Hill’s study of over five hundred self-made millionaires—a condensed, accessible explanation of his Law of Success philosophy, which includes thirteen steps to riches (financial, emotional, and spiritual).",
        "image": "selfhelp_subtle.jpg"
    },
    {
        "id": 25, "title": "The Mountain Is You", "author": "Brianna Wiest", "date": "2020",
        "category": "Self-help",
        "summary": "The Mountain Is You is a self-help book by Brianna Wiest that explains how to overcome self-sabotage by using the metaphor of a 'mountain' representing internal obstacles formed by conflicting needs and past trauma.",
        "full_content": " The book provides strategies for self-mastery, including identifying damaging behaviors, building emotional intelligence, and releasing trauma at a cellular level, ultimately guiding readers to transform self-sabotage into self-mastery.",
        "image": "selfhelp_grit.jpg"
    },

]

# --- Utility Functions for API Data Formatting ---

def get_grouped_data():
    """Formats MOCK_POSTS into the genre-grouped structure similar to the frontend"s blogData."""
    
    # Define descriptive texts for each genre (matching the frontend logic)
    genre_descriptions = {
        "Mystery/Thriller": {
            "genreTitle": "Mystery/Thriller: Dive into Suspense",
            "genreText": "Fictional mystery books are for anyone who enjoys suspense, problem-solving, and uncovering secrets — from kids to adults."
        },
        "Romance": {
            "genreTitle": "Romance: Love, Loss, and Connection",
            "genreText": "Soft romance novels focus on feelings, relationships, and personal growth rather than passion or heartbreak."
        },
        "Science Fiction": {
            "genreTitle": "Science: Exploring the Universe and Humanity",
            "genreText": "Science books dive into astrophysics, biology, history, and human evolution to define our place in the cosmos."
        },
        "Historical Fiction": {
            "genreTitle": "Historical Fiction: Echoes of the Past",
            "genreText": "Books based on true historical events are for readers who want to feel connected to the real stories of humanity — our struggles, triumphs, and lessons through time."
        },
        "Self-help": {
            "genreTitle": "Self-Help: Tools for Growth",
            "genreText": "Self-help books are for anyone who wants to think better, feel better, and live better. They help you unlock your potential and live with confidence, peace, and purpose."
        }
    }
    
    grouped_data = {}
    
    # Group posts by category
    posts_by_category = defaultdict(list)
    for post in MOCK_POSTS:
        # Create simplified book object for the list view
        book_data = {
            "title": post["title"],
            "summary": post["summary"],
            "coverImage": post["image"]
        }
        posts_by_category[post["category"]].append(book_data)

    # Combine groups with descriptions
    for category, books in posts_by_category.items():
        if category in genre_descriptions:
            grouped_data[category] = {
                **genre_descriptions[category],
                "books": books
            }
        
    return grouped_data


# --- Standard Flask Routes (Serving HTML) ---

@app.route("/users")
def index():
    """Renders the main blog index page (placeholder)."""
    # NOTE: In a production environment, you would use "render_template("book_blog.html")".
    return "<h1>BookPaglu Backend Running</h1><p>API endpoints are active at /api/...</p>"


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    """Renders a single post page with full content."""
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        abort(404)

    POST_HTML = f"""
    <h1>{post["title"]}</h1>
    <p>By: {post["author"]} on {post["date"]}</p>
    <span style="background-color: #e0e7ff; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{post["category"]}</span>
    <hr style="margin: 15px 0;">
    <p>{post["full_content"]}</p>
    <a href="/">Back to Home</a>
    """
    return render_template_string(POST_HTML, post=post)


# --- API Endpoints (Returning JSON) ---

@app.route("/api/data", methods=["GET"])
def api_data():
    """
    API Endpoint 1: Returns the entire blog data grouped by genre.
    (This structure is ideal for fetching data to replace the local JS "blogData" object.)
    """
    grouped_data = get_grouped_data()
    return jsonify(grouped_data)

@app.route("/api/genres", methods=["GET"])
def api_genres():
    """
    API Endpoint 2: Returns a list of all available genres.
    """
    genres = sorted(list(set(post["category"] for post in MOCK_POSTS)))
    return jsonify(genres)

@app.route("/api/books", methods=["GET"])
def api_books():
    """
    API Endpoint 3: Returns all books. Can be filtered by genre using a query parameter.
    Example: /api/books?genre=Romance
    """
    genre_filter = request.args.get("genre")

    if genre_filter:
        # Normalize category names for matching (e.g., handles spaces/slashes)
        normalized_filter = genre_filter.lower().replace("/", "").replace(" ", "")
        
        filtered_posts = [
            post for post in MOCK_POSTS 
            if post["category"].lower().replace("/", "").replace(" ", "") == normalized_filter
        ]
        return jsonify(filtered_posts)
    
    return jsonify(MOCK_POSTS)

@app.route("/api/books/<int:book_id>", methods=["GET"])
def api_book_detail(book_id):
    """
    API Endpoint 4: Returns the details for a single book.
    Example: /api/books/1
    """
    book = next((p for p in MOCK_POSTS if p["id"] == book_id), None)

    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    return jsonify(book)

# Run the application
if __name__ == "_main_":
    app.run(debug=True)