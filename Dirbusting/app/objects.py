# class Book:
#     def __init__(self, name, author, publisher, description, price, image):
#         self.name = name
#         self.author = author
#         self.description = description
#         self.publisher = publisher
#         self.price = price
#         self.image = image
        

# #And our list of books

# bookList = {}

from .models import *

def populateBookTable():

    linBasic = Item(name="Linux Basics for Hackers , Getting Started with Networking, Scripting, and Security in Kali",
                    category="book",
                    #author="Occupy the Web",
                    #publisher="No Starch Press",
                    description="""
Many aspiring hackers are unfamiliar with Linux, having learned computer basics in a Windows or Mac environment. This can pose the single most important obstacle to mastering the skills to becoming a better hacker; while hacking can be done with Windows or OS X, nearly all hacking tools are developed specifically for Linux. Linux Basics for Hackers aims to provide you with a foundation of Linux skills that every hacker needs. As you progress, you'll have access to numerous real-world examples and hands-on exercises to apply your new knowledge and bring yourself up to speed.

""",
                    price=14.95,
                    image="images/LinuxBasics.jpg"
                    )


    webApp = Item(name="The Web Application Hacker′s Handbook: Finding and Exploiting Security Flaws",
                  category="book",
                  #author="Dafydd Stuttard",
                  #publisher="Wiley",
                  description="""
Web applications are the front door to most organizations, exposing them to attacks that may disclose personal information, execute fraudulent transactions, or compromise ordinary users. This practical book has been completely updated and revised to discuss the latest step-by-step techniques for attacking and defending the range of ever-evolving web applications. You'll explore the various new technologies employed in web applications that have appeared since the first edition and review the new attack techniques that have been developed, particularly in relation to the client side.
""",
                  price=35.00,
                  image="images/WebAppHackers.jpg"
                  )


    rookies = Item(name="Python for Rookies",
                   category="book",
                   description="""
Python for Rookies is designed to help students learn how to program. Using the Python language as a tool, the approach taken teaches students the fundamentals of programming and re-enforces good programming practice. Written for students studying a variety of degree subjects such as Games Technology, Creative Computing and Multimedia (where core Computer Science is applied to the Arts) the pace and breadth would also be suitable for a one semester introductory programming course for all computing undergraduates. We hope that the example programs, chosen to enliven and motivate will also be very relevant to a range of courses and the varied ambitions of people who need to acquire programming skills. The book covers programming from small script-style applications to larger pieces of software. The emphasis remains on problem-solving, even through the introduction of common libraries
""",
                   price=26.51,
                   image="images/rookies.jpg",
                   hidden=True
                   )
                   
    
    bhPython = Item(name="Black Hat Python: Python Programming for Hackers and Pentesters",
                    category="book",
                    #author="Justin Seitz",
                    #publisher="No Starch Press",
                    description="""
When it comes to creating powerful and effective hacking tools, Python is the language of choice for most security analysts. But just how does the magic happen?
                    
In Black Hat Python, the latest from Justin Seitz (author of the best-selling Gray Hat Python), you’ll explore the darker side of Python’s capabilities—writing network sniffers, manipulating packets, infecting virtual machines, creating stealthy trojans, and more.

""",
                    price=18.99,
                    image="images/BlackHat.jpg"
                    )


    
    ghHackers = Item(name="Gray Hat Hacking: The Ethical Hacker's Handbook, Fifth Edition",
                     category="book",
                     #author="Allen Harper",
                     #publisher="McGraw-Hill Education",
                     description="""

Fortify your network and avert digital catastrophe with proven strategies from a team of security experts. Completely updated and featuring 13 new chapters, Gray Hat Hacking: The Ethical Hacker’s Handbook, Fifth Edition explains the enemy’s current weapons, skills, and tactics and offers field-tested remedies, case studies, and ready-to-try testing labs. Find out how hackers gain access, overtake network devices, script and inject malicious code, and plunder Web applications and browsers. Android-based exploits, reverse engineering techniques, and cyber law are thoroughly covered in this state-of-the-art resource.
""",
                     price=28.99,
                     image="images/GrayHat.jpg"
                     )

    db.session.add(linBasic)
    db.session.add(webApp)
    db.session.add(rookies)
    db.session.add(bhPython)
    db.session.add(ghHackers)
    db.session.commit()


def populateUserTable():

    bernard = User(name="bernard",
                   email="bernard@blackbooks.net",
                   password="nipsey",
                   level="admin")

    manny = User(name="manny",
                 email="manny@blackbooks.net",
                 password="lavender",
                 )

    fran = User(name="fran",
                email="fran@blackbooks.net",
                password="katzenjammer")

    db.session.add(bernard)
    db.session.add(manny)
    db.session.add(fran)
    db.session.commit()
    
#    userlist = {"bernard@blackbooks.net": "nipsey",
#                "manny@blackbooks.net": "calm",
#                "fran@blackbooks.net", "Katzenjammer")
