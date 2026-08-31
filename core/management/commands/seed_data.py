from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
import random

from users.models import User
from posts.models import Post, Like, Bookmark
from comments.models import Comment


class Command(BaseCommand):
    help = "Seed the database with realistic demo data"

    def handle(self, *args, **options):

        self.stdout.write("Seeding database...")

        # Clear existing data
        Like.objects.all().delete()
        Bookmark.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        User.objects.all().delete()

        # Create users
        users = self.create_users()

        # Create posts
        posts = self.create_posts(users)

        # Create comments
        self.create_comments(users, posts)

        # Create likes
        self.create_likes(users, posts)

        # Create bookmarks
        self.create_bookmarks(users, posts)

        self.stdout.write(
            self.style.SUCCESS(
                "Database seeded successfully!"
            )
        )

    def create_users(self):
        users_data = [
            {
                "username": "ahmed_dev",
                "email": "ahmed.dev@example.com",
                "password": "Password123!",
                "first_name": "Ahmed",
                "last_name": "Hassan",
                "bio": "Backend developer and tech enthusiast.",
            },
            {
                "username": "omar_codes",
                "email": "omar.codes@example.com",
                "password": "Password123!",
                "first_name": "Omar",
                "last_name": "Ali",
                "bio": "Software engineer who loves clean code.",
            },
            {
                "username": "sara_designs",
                "email": "sara.designs@example.com",
                "password": "Password123!",
                "first_name": "Sara",
                "last_name": "Mohamed",
                "bio": "UI designer exploring modern web apps.",
            },
            {
                "username": "youssef_cs",
                "email": "youssef.cs@example.com",
                "password": "Password123!",
                "first_name": "Youssef",
                "last_name": "Adel",
                "bio": "Computer science student and developer.",
            },
            {
                "username": "mariam_dev",
                "email": "mariam.dev@example.com",
                "password": "Password123!",
                "first_name": "Mariam",
                "last_name": "Samir",
                "bio": "Full stack developer and problem solver.",
            },
            {
                "username": "karim_tech",
                "email": "karim.tech@example.com",
                "password": "Password123!",
                "first_name": "Karim",
                "last_name": "Mostafa",
                "bio": "Technology lover and software builder.",
            },
        ]

        users = []

        for data in users_data:
            user = User.objects.create(
                username=data["username"],
                email=data["email"],
                password=make_password(data["password"]),
                first_name=data["first_name"],
                last_name=data["last_name"],
                bio=data["bio"],
            )

            users.append(user)

        return users


    def create_posts(self, users):
        posts_data = [
            # Ahmed
            {
                "title": "What I Learned Building My First Django API",
                "author": users[0],
                "content": """
    Building my first Django API completely changed the way I understood
    web development. Before working on the project, I knew the basic concepts
    of HTTP requests, databases, and backend applications, but I had never
    connected all of these pieces together in one real application.

    The first thing I learned was how important it is to organize a backend
    project properly. Separating models, serializers, views, URLs, and business
    logic makes the application much easier to understand and maintain. It also
    makes debugging much less painful when something goes wrong.

    Another important lesson was working with databases. Creating relationships
    between users, posts, and comments helped me understand why database design
    matters before writing the actual application logic. A small decision in the
    model structure can affect many parts of the application later.

    Authentication was another interesting part of the process. Understanding
    how users log in, how tokens are created, and how protected endpoints verify
    those tokens gave me a much better understanding of what happens behind the
    scenes when someone uses a modern web application.

    The biggest lesson was that building a real project is very different from
    following a tutorial. Problems appear everywhere, and solving those problems
    is where most of the actual learning happens. Django made it easier to build
    the application, but understanding why each part exists was even more valuable.
    """,
            },
            {
                "title": "Why Backend Development Is More Than Writing APIs",
                "author": users[0],
                "content": """
    When I first started learning backend development, I thought most of the job
    was about creating endpoints and returning JSON responses. After building
    several small applications, I realized that APIs are only one part of the
    backend.

    A good backend also needs a clear data model, proper authentication,
    authorization, validation, error handling, and a structure that can grow as
    the application becomes larger. An endpoint can work perfectly and still be
    part of a badly designed system if the surrounding architecture is difficult
    to maintain.

    Database design is especially important. Choosing the right relationships
    between entities can make queries simpler and prevent duplicated information.
    It is also important to think about what happens when records are deleted,
    updated, or no longer available.

    Security should also be considered from the beginning. Passwords should never
    be stored as plain text, protected resources should require authentication,
    and users should only be allowed to perform actions they are authorized to do.

    The more projects I build, the more I understand that backend development is
    really about designing reliable systems. Writing the code is important, but
    thinking about how the system behaves in different situations is what makes
    the difference between a working application and a maintainable one.
    """,
            },
            {
                "title": "Understanding REST APIs as a Beginner",
                "author": users[0],
                "content": """
    REST APIs were one of the first backend concepts that really helped me
    understand how frontend and backend applications communicate. At first,
    methods such as GET, POST, PATCH, and DELETE looked like simple HTTP details,
    but they actually provide a clear structure for interacting with resources.

    A GET request can be used to retrieve information, while POST is commonly used
    to create new resources. PATCH is useful when only part of an existing resource
    needs to be changed, and DELETE removes a resource when the application allows
    that operation.

    One thing that helped me understand REST was thinking about resources instead
    of pages. Instead of creating endpoints that describe what the application
    should do, it is often cleaner to design endpoints around resources such as
    users, posts, and comments.

    Status codes are also an important part of the API design. Returning the
    correct status code helps the frontend understand whether a request succeeded,
    failed because of invalid input, or failed because the user is not authorized.

    REST APIs are simple enough to start with, but building a good API requires
    more than memorizing HTTP methods. Consistency, validation, authentication,
    error handling, and clear response structures all contribute to the quality
    of an API.
    """,
            },
            {
                "title": "Things I Wish I Knew Before Learning PostgreSQL",
                "author": users[0],
                "content": """
    When I started learning PostgreSQL, I initially focused on writing queries
    and understanding basic SQL syntax. That was useful, but I later realized
    that understanding relational databases requires a much broader perspective.

    Tables, primary keys, foreign keys, indexes, and relationships are not just
    technical features. They are tools for representing real information in a
    structured way. Once I started designing databases for actual applications,
    these concepts became much easier to understand.

    Relationships were especially important for me. A user can create many posts,
    and each post can have many comments. Representing these relationships properly
    makes it possible to retrieve the required information without duplicating
    data across multiple tables.

    Indexes were another concept that became more meaningful after working with
    larger datasets. An index can significantly improve query performance, but
    indexes also have costs, so they should be used intentionally rather than
    added everywhere.

    The most useful advice I can give another beginner is to practice database
    design with real projects. Writing SQL queries is important, but understanding
    why the database should be structured in a particular way is even more valuable.
    """,
            },
            {
                "title": "How Git Changed the Way I Work on Projects",
                "author": users[0],
                "content": """
    Git became much more useful to me when I stopped thinking about it as simply
    a tool for uploading code to GitHub. It is actually a way to manage the history
    of a project and work safely while making changes.

    Branches allow developers to experiment with new features without immediately
    changing the main version of the application. This becomes especially useful
    when several features are being developed at the same time.

    Commit messages are also more important than I originally thought. A clear
    commit history makes it easier to understand what changed and why a particular
    decision was made. It can also make debugging much easier when a problem is
    introduced by a recent change.

    Pull requests and code reviews add another useful layer. They encourage
    developers to look at their work from another perspective and catch problems
    before changes reach the main branch.

    The biggest benefit for me is confidence. Knowing that I can create a branch,
    experiment, and return to an earlier version makes it much easier to work on
    large features without being afraid of breaking everything.
    """,
            },

            # Omar
            {
                "title": "Writing Cleaner Code in Real Projects",
                "author": users[1],
                "content": """
    Clean code is one of those topics that sounds simple until you work on a
    project that contains hundreds or thousands of lines. A piece of code can
    work correctly and still be difficult for another developer to understand.

    One of the first things I started paying attention to was naming. Variables,
    functions, and classes should communicate their purpose clearly. Good names
    reduce the amount of explanation required when reading the code.

    Another important principle is keeping functions focused. When a function is
    responsible for authentication, validation, database operations, and response
    formatting at the same time, it quickly becomes difficult to test and maintain.

    I also learned that comments should not be used to explain every line of code.
    When the code is written clearly, comments can be reserved for decisions that
    are not obvious from the implementation itself.

    Clean code is not about making everything look perfect. It is about reducing
    unnecessary complexity and making future changes easier. This becomes more
    important as a project grows and more developers start working on it.
    """,
            },
            {
                "title": "The Difference Between Authentication and Authorization",
                "author": users[1],
                "content": """
    Authentication and authorization are two concepts that are often confused
    when someone is starting backend development. They are related, but they solve
    different problems.

    Authentication answers the question: who are you? A login system verifies
    the user's credentials and establishes their identity. Modern applications
    often use tokens or sessions to keep track of that authenticated user.

    Authorization comes after authentication. It answers the question: what are
    you allowed to do? A user may be authenticated but still not have permission
    to edit another user's post or access an administrator-only resource.

    This distinction became much clearer when I implemented protected endpoints.
    Checking whether a token is valid is not enough. The application also needs to
    check whether the authenticated user owns the resource or has the required
    permissions.

    Keeping authentication and authorization separate makes the security logic
    easier to understand. It also makes it easier to add roles or permissions later
    without rewriting the entire authentication system.
    """,
            },
            {
                "title": "How I Approach Debugging Backend Problems",
                "author": users[1],
                "content": """
    Debugging used to feel like randomly changing code until the error disappeared.
    Over time, I developed a more structured approach that makes backend problems
    much easier to solve.

    The first step is understanding the exact error. Instead of immediately
    searching for the error message, I try to identify which part of the request
    failed and what the application was expected to do.

    Logs are extremely useful during this process. Printing the values involved
    in a failing operation can reveal problems that are not obvious from the
    error message alone. Network tools and API clients can also show the exact
    request and response.

    I also try to reproduce the problem consistently. If an issue only happens
    sometimes, it is much harder to identify the cause. Once the problem can be
    reproduced, I can change one thing at a time and verify whether the behavior
    changes.

    The most important lesson is to avoid guessing. Debugging becomes much faster
    when each change is based on evidence from the application rather than a random
    attempt to fix the problem.
    """,
            },
            {
                "title": "Why Error Handling Matters in Backend Systems",
                "author": users[1],
                "content": """
    A backend application will eventually encounter invalid input, missing data,
    database failures, expired authentication tokens, and unexpected situations.
    Good error handling is what allows the application to respond to these cases
    without becoming unpredictable.

    One common mistake is returning the same generic error for every situation.
    The frontend needs enough information to understand whether the request failed
    because the user is unauthorized, the resource does not exist, or the submitted
    data is invalid.

    At the same time, error responses should not expose sensitive internal
    information. Database errors and stack traces may be useful during development,
    but they should not be returned directly to users in a production application.

    Consistent error responses also make frontend development easier. When every
    endpoint follows a predictable structure, the frontend can display useful
    messages without having to handle every endpoint differently.

    Error handling is not something that should be added at the end of a project.
    Thinking about failure cases while designing each feature leads to a much more
    reliable application.
    """,
            },
            {
                "title": "What Makes an API Easy to Maintain",
                "author": users[1],
                "content": """
    An API can be functional and still be difficult to maintain. As an application
    grows, developers need to understand existing endpoints quickly and safely
    make changes without breaking unrelated features.

    Consistency is one of the most important factors. Similar resources should
    follow similar URL patterns, HTTP methods, response structures, and error
    formats. This reduces the amount of knowledge developers need to remember.

    Validation should happen close to the boundary of the application. Invalid
    data should be rejected before it reaches deeper business logic or the database.

    Another useful practice is keeping responsibilities separated. Controllers
    should not become enormous files containing every piece of business logic.
    When responsibilities are separated clearly, individual parts become easier
    to test and modify.

    Documentation also matters. Even a simple README describing authentication,
    main endpoints, and expected request formats can save developers significant
    time when they return to the project later.
    """,
            },

            # Sara
            {
                "title": "Designing Better User Interfaces for Developers",
                "author": users[2],
                "content": """
    A good user interface is not only about choosing attractive colors and fonts.
    It is mainly about helping users understand what they can do and what will
    happen when they interact with the application.

    Clear hierarchy is one of the first things I consider when designing a page.
    Titles should be easy to identify, important actions should stand out, and
    secondary information should not compete with the main content.

    Spacing is another detail that can dramatically improve a design. When
    elements are too close together, the interface feels crowded. Consistent
    spacing gives each section room to breathe and makes the page easier to scan.

    Buttons and forms also need clear states. Users should be able to tell when
    a button is disabled, when a request is loading, and when an action succeeded
    or failed.

    The best interfaces usually feel simple because they remove unnecessary
    decisions. Good design is often less about adding more elements and more about
    making the existing elements easier to understand.
    """,
            },
            {
                "title": "Why Responsive Design Should Be Planned Early",
                "author": users[2],
                "content": """
    Responsive design is much easier when it is considered from the beginning
    rather than treated as a final step. A layout that looks perfect on a desktop
    can quickly become difficult to use on a smaller screen.

    I usually start by thinking about content and hierarchy instead of specific
    screen sizes. The important question is how the interface should adapt when
    there is less horizontal space.

    Flexible layouts, relative units, and well-designed breakpoints can make a
    large difference. Cards may stack vertically, navigation may become smaller,
    and text may need different spacing on mobile devices.

    Touch interaction is also important. Buttons and links should have enough
    space around them so users can interact with them comfortably on a phone.

    Testing at different widths throughout development saves a lot of time.
    Responsive design becomes much harder when dozens of fixed desktop assumptions
    have already been built into the interface.
    """,
            },
            {
                "title": "Small CSS Details That Improve a Website",
                "author": users[2],
                "content": """
    Sometimes the biggest visual improvements come from small changes rather than
    a complete redesign. Consistent spacing, border radius, typography, and button
    styles can make an application feel much more polished.

    Typography is especially important because it affects how easily users can
    read the content. A clear hierarchy between headings, paragraphs, labels, and
    secondary text makes long pages much easier to scan.

    Cards can also benefit from subtle visual separation. A simple border,
    appropriate padding, and consistent spacing often work better than adding
    too many shadows or decorative elements.

    Another useful improvement is keeping repeated components consistent. If every
    button behaves and looks differently, the application feels unfinished even
    when each individual button looks good.

    Good CSS is often about consistency. Once the visual rules are established,
    applying them across the whole application creates a much more professional
    result.
    """,
            },
            {
                "title": "How Good Empty States Improve User Experience",
                "author": users[2],
                "content": """
    Empty states are easy to ignore because they only appear when there is no data.
    However, they are an important part of the user experience because they tell
    users what is happening and what they can do next.

    A completely empty page can make users think that something is broken. A good
    empty state explains why there is no content and, when possible, provides an
    action that helps the user move forward.

    For example, an empty bookmarks page could explain that saved posts will appear
    there and provide a link back to the main feed. This is much more helpful than
    simply displaying a blank area.

    Loading and error states should receive the same attention. Users need feedback
    when the application is waiting for a response or when something went wrong.

    Thinking about these states during design makes the interface feel complete
    instead of designing only for the successful scenario.
    """,
            },
            {
                "title": "Making Blog Cards Easier to Scan",
                "author": users[2],
                "content": """
    Blog cards have limited space, so the challenge is showing enough information
    without overwhelming the user. The title, author, date, and a short preview
    usually provide enough context for someone to decide whether they want to
    open the article.

    Long content should normally be truncated on the card instead of displaying
    the entire article. This keeps cards at a predictable height and allows users
    to scan several posts quickly.

    Visual hierarchy helps here. The title should attract attention first, followed
    by the preview and metadata. Secondary information should be visually quieter
    so it does not compete with the article title.

    Consistent card dimensions are also useful when multiple posts appear in a
    grid. Even when articles have different lengths, the feed can remain organized
    and easy to browse.

    A well-designed card does not need to show everything. Its job is to provide
    enough information to help the user decide whether to continue reading.
    """,
            },

            # Youssef
            {
                "title": "My Experience Learning Data Structures",
                "author": users[3],
                "content": """
    Learning data structures changed the way I think about programming. Before
    studying them seriously, I mostly focused on getting a program to produce the
    correct result. Data structures introduced another question: how efficiently
    can the program produce that result?

    Arrays and linked lists helped me understand how data can be organized in
    different ways. Stacks and queues showed how choosing a structure based on
    access patterns can simplify a problem.

    Trees and hash tables were especially interesting because they demonstrated
    how different structures can dramatically change the performance of common
    operations. Understanding these ideas also made algorithm discussions much
    easier to follow.

    The most useful part of studying data structures was solving problems rather
    than memorizing definitions. Implementing structures myself forced me to
    understand how they work internally.

    I still encounter problems where the right data structure is not immediately
    obvious. However, having a strong foundation makes it easier to compare possible
    solutions and reason about their trade-offs.
    """,
            },
            {
                "title": "Why Building Projects Is Better Than Watching Tutorials",
                "author": users[3],
                "content": """
    Tutorials are useful when learning a new technology, but they can create a
    false feeling of understanding. It is easy to follow someone else's code and
    feel confident until you try to build the same feature without instructions.

    Projects force you to make decisions. You need to decide how models should be
    structured, how endpoints should behave, how errors should be handled, and how
    different features should communicate.

    You will also encounter problems that tutorials usually avoid. Dependencies
    may behave differently, a database query may fail, or a small configuration
    mistake may prevent the application from starting.

    These problems are not wasted time. They are part of learning how software
    development actually works. Searching for the cause, reading documentation,
    and testing possible solutions develops skills that watching videos cannot
    provide by itself.

    For me, the best learning process combines both approaches: use tutorials and
    documentation to understand concepts, then build something independently to
    prove that you actually understand them.
    """,
            },
            {
                "title": "Lessons From Building a Blog Application",
                "author": users[3],
                "content": """
    Building a blog application looks simple at first. A user creates an account,
    writes a post, and other users can read and comment on it. Once you start
    implementing the details, however, many interesting engineering problems appear.

    Authentication is one example. Users need to register and log in, but protected
    actions also need authorization. A user should be able to edit their own post
    without being able to edit someone else's.

    Database relationships are another important part. Users, posts, comments,
    likes, and bookmarks all have relationships that need to be represented
    correctly.

    The frontend also needs to handle loading states, errors, empty states, and
    different user interactions. A feature is not really finished just because
    the backend endpoint works.

    The project taught me that software development is mostly about connecting
    many small pieces into a system that behaves consistently. Each individual
    feature may be simple, but making all of them work together requires careful
    planning and testing.
    """,
            },
            {
                "title": "How I Organize My Learning as a CS Student",
                "author": users[3],
                "content": """
    Learning computer science can become overwhelming because there are so many
    technologies, frameworks, and concepts available. I found that having a clear
    learning structure makes the process much easier.

    I try to separate fundamentals from tools. Programming concepts, data
    structures, databases, networking, and software design remain useful even when
    the framework I am using changes.

    After learning a concept, I prefer to build something small with it. This
    creates a connection between theory and implementation and makes it easier
    to remember later.

    I also keep track of problems I encounter during projects. Writing down what
    went wrong and how I fixed it creates a personal collection of debugging
    experience that becomes surprisingly useful over time.

    The goal is not to learn everything at once. Consistent progress and practical
    experience are more valuable than trying to master several technologies at
    the same time.
    """,
            },
            {
                "title": "What I Learned From My First Backend Project",
                "author": users[3],
                "content": """
    My first backend project taught me that the difficult part of development is
    often not writing the first version of a feature. The difficult part is making
    that feature reliable when users do unexpected things.

    A form can send invalid data. A requested resource may not exist. A user may
    try to access another user's information. A database operation may fail.
    Thinking about these cases changes the way you design the application.

    I also learned the importance of testing APIs independently from the frontend.
    Using an API client makes it much easier to understand whether a problem comes
    from the backend or from the way the frontend is communicating with it.

    Project structure became another important lesson. When everything is placed
    in a few large files, adding new features becomes increasingly difficult.
    Separating responsibilities early saves time later.

    Most importantly, the project gave me confidence. After building something
    from start to finish, backend concepts that once felt abstract became much
    easier to understand.
    """,
            },

            # Mariam
            {
                "title": "Building Features That Work Together",
                "author": users[4],
                "content": """
    One of the biggest challenges in application development is not building
    individual features but making sure those features work correctly together.
    Authentication, posts, comments, profiles, and other parts of an application
    usually depend on each other.

    For example, a comment feature depends on an authenticated user and an existing
    post. Editing a post depends on both authentication and authorization. The
    frontend needs to know which actions are available to the current user.

    This means that feature development should include thinking about integration.
    A backend endpoint may be correct by itself but still cause problems if its
    response does not match what the frontend expects.

    I have found that testing complete user flows is extremely useful. Instead of
    testing only whether an endpoint returns a successful response, I try to
    simulate what a real user would do from beginning to end.

    This approach reveals problems that isolated testing can miss and creates a
    much stronger final application.
    """,
            },
            {
                "title": "Why Database Relationships Matter",
                "author": users[4],
                "content": """
    Database relationships become much easier to understand when working on an
    application with real features. A simple blog already contains several
    relationships: users create posts, posts have comments, and users can interact
    with posts.

    The goal of a relational design is to store information without unnecessary
    duplication while still making common queries practical.

    Foreign keys provide a clear connection between related records. They also
    allow the database and application to enforce rules about what data belongs
    together.

    Deletion behavior is another decision that should not be ignored. Depending
    on the relationship, deleting a record may require deleting related records,
    preserving them, or marking them as deleted.

    Designing these relationships before writing a large amount of application
    code can prevent many problems later. The database is not just storage; it is
    an important part of the application's architecture.
    """,
            },
            {
                "title": "How I Handle Feature Development",
                "author": users[4],
                "content": """
    When I start a new feature, I try not to immediately begin writing code.
    First, I define what the feature should do and identify the data involved.

    Then I think about the backend requirements, including models, validation,
    authentication, authorization, and API behavior. After that, I consider how
    the frontend will consume the feature.

    Breaking a feature into smaller tasks makes the implementation much easier.
    Instead of thinking about a large requirement such as "build comments", I can
    separate it into creating comments, retrieving comments, updating them,
    deleting them, and handling permissions.

    Testing each part while developing also reduces the number of problems at the
    end. It is much easier to fix a small issue immediately than to debug several
    interacting problems later.

    This process may feel slower at the beginning, but it usually saves time and
    produces more reliable features.
    """,
            },
            {
                "title": "The Importance of Validation in Web Applications",
                "author": users[4],
                "content": """
    Validation is one of those backend responsibilities that users rarely notice
    when it works correctly. Its purpose is to make sure the application only
    accepts data that makes sense.

    Client-side validation is useful because it provides immediate feedback, but
    it should never be the only layer of validation. A malicious or modified
    request can bypass frontend checks completely.

    Server-side validation protects the application by checking incoming data
    before it reaches business logic or the database. Required fields, maximum
    lengths, formats, and allowed values are examples of common validation rules.

    Good validation messages are also important. Instead of simply saying that a
    request failed, the application should explain which field needs attention
    when it is safe to do so.

    Strong validation creates predictable data and prevents many bugs before they
    can spread through the rest of the application.
    """,
            },
            {
                "title": "What Makes a Software Project Feel Complete",
                "author": users[4],
                "content": """
    A project can have all the required features and still feel unfinished.
    Completeness is not only about functionality; it is also about the details
    around those features.

    Loading states, error messages, empty states, responsive layouts, and consistent
    UI components all contribute to the final experience. These details become
    especially visible when someone else tries the application for the first time.

    Backend quality matters too. Clear errors, proper validation, authentication,
    authorization, and a well-organized codebase make the project easier to trust
    and maintain.

    Documentation is another part that is often forgotten. A clear README with
    setup instructions, technologies, and important API information makes the
    project much easier for another developer to understand.

    The final polishing stage is where a functional project becomes a project
    that is worth showing to other people.
    """,
            },

            # Karim
            {
                "title": "Why Software Engineering Requires More Than Coding",
                "author": users[5],
                "content": """
    Programming is obviously an important part of software engineering, but it is
    only one part of the job. Building reliable software requires understanding
    requirements, designing systems, testing behavior, and communicating decisions.

    A developer needs to think about what users actually need before deciding how
    to implement a feature. A technically impressive solution is not useful if it
    does not solve the right problem.

    Testing is another important part of engineering. Manual testing can catch
    many issues, but automated tests provide a repeatable way to verify important
    behavior as the project changes.

    Version control and documentation also contribute to engineering quality.
    Software is usually maintained for much longer than it takes to write the
    first version, so future developers need to understand how the system works.

    The more I learn, the more I see coding as a tool rather than the entire
    discipline. Good engineering is about building software that remains useful,
    understandable, and reliable over time.
    """,
            },
            {
                "title": "Understanding the Role of HTTP in Web Development",
                "author": users[5],
                "content": """
    HTTP is one of the foundations of modern web applications. Every time a
    frontend communicates with a backend, HTTP provides the rules for sending
    requests and receiving responses.

    Understanding methods such as GET, POST, PUT, PATCH, and DELETE makes API
    development much easier. Each method communicates an intended type of
    operation and helps keep APIs predictable.

    Headers are also important. They can contain information about content types,
    authentication credentials, caching, and other aspects of a request.

    Status codes provide another layer of communication. A successful response,
    a validation error, an unauthorized request, and a missing resource should
    not all look the same.

    Learning HTTP at a deeper level helped me understand what frameworks are doing
    behind the scenes. Frameworks make development easier, but knowing the protocol
    underneath them makes debugging and API design much more straightforward.
    """,
            },
            {
                "title": "Choosing Between SQL and NoSQL Databases",
                "author": users[5],
                "content": """
    The SQL versus NoSQL discussion can make database selection sound like a
    competition where one technology must always be better. In reality, the right
    choice depends on the application's requirements.

    Relational databases are excellent when data has clear relationships and
    consistency is important. Their structured schema and powerful query language
    make them a strong choice for many business applications.

    NoSQL databases can be useful when the data model is more flexible or when
    certain access patterns benefit from document-based storage. They can also
    work well for applications where the schema changes frequently.

    The important lesson is to understand the requirements before choosing the
    technology. Data relationships, query patterns, transaction requirements,
    scale, and team experience all matter.

    Learning both approaches is valuable because it teaches developers to think
    about data independently from a specific database product.
    """,
            },
            {
                "title": "How I Use Documentation When Learning Technology",
                "author": users[5],
                "content": """
    Documentation is one of the most useful resources for developers, but it can
    feel difficult to read when learning a new technology. I used to rely heavily
    on tutorials and examples, but official documentation became much more useful
    once I learned how to navigate it.

    I usually start with the quick-start section to understand the basic workflow.
    After that, I look for the reference documentation when I need precise
    information about a specific function, class, option, or configuration.

    Examples are helpful, but I try not to copy them blindly. Understanding why
    the example works makes it much easier to adapt it to a different project.

    Documentation is also often more reliable than random answers on the internet,
    especially when a framework changes between versions.

    Developing the habit of reading documentation has made me more independent.
    Instead of waiting for someone to explain every problem, I can usually find
    the information I need and verify how the technology is intended to work.
    """,
            },
            {
                "title": "What I Look for Before Calling a Project Finished",
                "author": users[5],
                "content": """
    Before considering a project finished, I like to test it from the perspective
    of someone who has never seen the code before. This often reveals problems
    that are easy to miss during development.

    I check the main user flows first. Registration, login, creating content,
    editing, deleting, and interacting with existing content should all work
    without unexpected behavior.

    Then I test invalid scenarios. What happens if a required field is missing?
    What if the requested resource does not exist? What if a user tries to perform
    an action they do not have permission to perform?

    I also check the visual side of the application. Layout consistency, responsive
    behavior, readable content, and clear feedback are important parts of the
    experience.

    Finally, I review the code and documentation. Removing unused code, checking
    configuration, and writing clear setup instructions can make a big difference
    when the project is shared with someone else.
    """,
            },
        ]

        posts = []

        for data in posts_data:
            post = Post.objects.create(
                title=data["title"],
                slug=f"{slugify(data['title'])[:45]}-{len(posts) + 1}",
                content=data["content"].strip(),
                author=data["author"],
            )

            posts.append(post)

        return posts


    def create_comments(self, users, posts):
        comments_data = [
            "This is a really useful explanation. I especially liked the practical examples.",
            "I had a similar experience when I started working on my first project.",
            "The part about keeping the code maintainable is very important.",
            "Great post! This made the concept much easier to understand.",
            "I completely agree. Building projects is where most of the real learning happens.",
            "This is something I wish I had understood earlier.",
            "The database design section was particularly interesting. Good point.",
            "I think authentication and authorization are often confused by beginners.",
            "Have you tried applying this approach to a larger project?",
            "This is a great reminder that working code is not always good code.",
            "The explanation is simple but still covers the important details.",
            "I ran into the same problem recently, and documenting the solution helped me a lot.",
            "I really like the way you connected the theory with a real project.",
            "Would you recommend learning this before starting a framework?",
            "This is exactly the kind of practical advice developers need.",
            "The point about testing different scenarios is easy to overlook.",
            "I started paying more attention to this after working on a team project.",
            "Clear and well-written explanation. Looking forward to more posts like this.",
            "I never thought about this problem from that perspective before.",
            "The examples make the topic much easier to follow.",
            "This would be useful for anyone building their first backend application.",
            "I agree with the idea of learning fundamentals before focusing too much on tools.",
            "One of the biggest lessons I learned was also that debugging takes a lot of patience.",
            "The section about responsive design is especially relevant for modern applications.",
            "Good explanation. I would be interested in seeing how you handle this in production.",
            "This is a problem I have faced several times while building small applications.",
            "I like that you mentioned the importance of consistency across the project.",
            "Definitely agree that documentation becomes more important as the project grows.",
            "This is a great example of why software engineering is more than just writing code.",
            "I learned something new from this post. Thanks for sharing your experience.",
        ]

        random_generator = random.Random(42)

        for post in posts:
            number_of_comments = random_generator.randint(10, 15)

            # Don't allow the post author to comment on their own post.
            available_authors = [
                user for user in users
                if user.id != post.author.id
            ]

            selected_comments = random_generator.sample(
                comments_data,
                number_of_comments
            )

            for content in selected_comments:
                author = random_generator.choice(available_authors)

                Comment.objects.create(
                    content=content,
                    author=author,
                    post=post,
                )


    def create_likes(self, users, posts):
        random_generator = random.Random(100)

        for post in posts:
            available_users = users.copy()

            number_of_likes = random_generator.randint(3, 8)

            selected_users = random_generator.sample(
                available_users,
                min(number_of_likes, len(available_users))
            )

            for user in selected_users:
                Like.objects.create(
                    user=user,
                    post=post,
                )

    def create_bookmarks(self, users, posts):
        random_generator = random.Random(200)

        for post in posts:
            number_of_bookmarks = random_generator.randint(1, 4)

            selected_users = random_generator.sample(
                users,
                min(number_of_bookmarks, len(users))
            )

            for user in selected_users:
                Bookmark.objects.create(
                    user=user,
                    post=post,
                )