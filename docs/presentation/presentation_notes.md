# Presentation Notes

- 15 minutes talk (up to 20)
- One member
- Record:
  - video with slides and the audio
  - audio of presenter with indication of when to switch to next slide
- Can have multiple members record
- Recommendations for good presentation
  - Have some motivation and make the problem interesting (first 3 slides)
  - give a description of the problem after initial motivation (first 3 slides)
  - mention at a high level some of the conclusions of the work (first 3 slides)
  - Lots of Figures and Images, less words
- Sections:
  - Intro from previous part
  - Approach
  - Experiments
  - Results
  - Final Discussion
- Basically a less formal paper
- Have lots of figures (think if something can be conveyed visually)
- Each member submits slides and each member submits video

## Presentation

### Intro

- Reinforcement learning is an important type of machine learning
- Introduce AlphaGo
- Try to create an algorithm that uses AlphaGo's implementation
- AlphaGo
  - Training algorithm consists of 3 stages: self-play, training and pitting it
    against itself
  - two headed network to compute the value (roughly interpreted as winrate) of
    current game board, with policy to guide the next action
  - No true label for reinforcement learning
  - Monte Carlo Tree Search to get good estimate of the optimal policy
- Simplified network for AlphaGo implementation for snake
- DQN was saught as an alternative

### Approach

- Assumed Rules:
  - Collission with other snakes
  - Eating and staying above 0 health
  - Eating resets health to 100
  - health decreases every tick/movement
  - Board size 11x11
  - 1v3 or 4 snakes battle each other
  - Last snake alive is the winner

### Experiments

### Results

- What each iteration in the Alphanet means
-
- alternative: DQN and how it was used
- show some gifs

### Final Discussion

## Link to Presentation Slides

https://docs.google.com/presentation/d/1YZSXjmmI-R4RoHLmRIUN2RngWgEzjz-COcruYBCxTCk/edit?usp=sharing

link to folder

https://drive.google.com/open?id=1Knb5xECKhTKK9vVSAutyHNOFClFaFf8o
