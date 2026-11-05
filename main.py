import pygame
import random
import sys

# ---------------------------------------------------------
# 1. CORPUS DATA
# Students: Paste your book chapter or article text inside the triple quotes below!
# ---------------------------------------------------------
CORPUS = """
I've been trying for so long to sing you the right song
To show you something different every day
So you hear what I have to say, like puzzle pieces
And now we're here at a standstill
I wonder if you feel the kind of pain that rips your insides out
That's something I know all about
Shockin' ain't it?
Is it because I can't be her?
Made your mistakes and make me hurt
I can't fix you
Is it because I can't be her?
Made me awake and make me hurt
I can't fix you
[Drop]
I can't fix you
I can feel my heart breaking, mistakes I've been making
I'm running out of patience to pretend
This isn't how I'll let it end, my feigning fading
You've been mourning your loss here
And that's grinding my gears
How can a human lose their self-control?
There's nothing left to make you whole
I'm done explaining
Is it because I can't be her?
Made your mistakes and make me hurt
I can't fix you
Is it because I can't be her?
Made me awake and make me hurt
I can't fix you
Oh, oh-woah-oh-oh-oh
This is what happens when you leave it to somebody else
If you want it done right, you should just do it yourself
You oversaturate your world with nothing but machines
You might make everyone happy
But you're dead inside, just like me
And now we're here at a standstill
I wonder if you feel the kind of pain that rips your insides out
That's something I know all about
Shockin' ain't it?
We have a lot more in common than you would be calm with
It's like we're the same person, me and you
We both don't know what we can do
Is it because I can't be her?
Made your mistakes and make me hurt
I can't fix you
Is it because I can't be her?
Made me awake and make me hurt
I can't fix you
Is it because I can't be her?
Made your mistakes and make me hurt
I can't fix you
Is it because I can't be her?
Made me awake and make me hurt
I can't fix you
[Drop]
"""

def clean_and_tokenize(text):
    """Converts text to lowercase and splits it into a list of words."""
    words = text.split()
    for i, word in enumerate(words):
        words[i] = word.lower()
    return words

def build_bigrams(words):
    """Creates a dictionary where each word maps to a list of words that follow it."""
    bigrams = {}
    
    # ### TODO 2: Loop through the words list to build the bigram model.
    # You need to pair words[i] (current word) with words[i+1] (next word).
    # If the current word isn't in the dictionary yet, add it with an empty list.
    # Then append the next word to that list.
    for word in words:
        if word in bigrams:
            pass
        elif word not in bigrams:
            bigrams[word] = ""
    for i, word in enumerate(words):
        if i >= len(words) - 1:
            break
        bigrams[word] = words[i+1]

    return bigrams

def predict_next_word(current_word, bigrams):
    """Predicts the next word based on the current word using the bigram dictionary."""
    # ### TODO 3: Check if the current_word exists in our bigrams dictionary.
    # If it does, use random.choice() to select one word from its list of followers.
    # If it doesn't, return a random word from the dictionary keys to keep the chain going.
    temp = ""
    if current_word in bigrams:
        temp = random.choice(bigrams[current_word])
    else:
        temp = random.choice(list(bigrams))

    return temp

# ---------------------------------------------------------
# PYGAME WINDOW & ENGINE
# ---------------------------------------------------------
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Student Lab: 2-Gram Word Predictor")
font = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()

# Prepare the data
word_list = clean_and_tokenize(CORPUS)
bigram_dict = build_bigrams(word_list)

# Initial State
current_word = random.choice(word_list) if word_list else "the"
generated_text = current_word.capitalize()

# Timer setup: Triggers a new word automatically every 1000ms to bypass browser focus issues
AUTO_GEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AUTO_GEN_EVENT, 1000)

running = True
while running:
    screen.fill((30, 30, 30)) # Dark gray background
    
    # Render instructions
    instr_surface = font.render("Click inside the window OR wait to see text generate automatically!", True, (150, 150, 150))
    screen.blit(instr_surface, (20, 20))
    
    # Word wrap rendering logic
    words_to_draw = generated_text.split()
    x, y = 20, 80
    for word in words_to_draw:
        word_surface = font.render(word + " ", True, (255, 255, 255))
        if x + word_surface.get_width() > SCREEN_WIDTH - 20:
            x = 20
            y += 35  
        screen.blit(word_surface, (x, y))
        x += word_surface.get_width()

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Trigger text generation on automatic timer, mouse clicks, or key presses
        elif event.type == AUTO_GEN_EVENT or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            # Safely passes the validated bigram_dict variable
            next_word = predict_next_word(current_word, bigram_dict)
            generated_text += " " + next_word
            current_word = next_word

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
