"""NEAT Training for Flappy Bird - Bot A (Fixed)"""
import sys, os, time, pickle, json
from datetime import datetime

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import neat
import numpy as np
from flappy_env import FlappyBirdEnv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(base_dir, 'models'), exist_ok=True)
os.makedirs(os.path.join(base_dir, 'logs'), exist_ok=True)
os.makedirs(os.path.join(base_dir, 'results'), exist_ok=True)

LOG_FILE = os.path.join(base_dir, 'logs/neat_training.log')
RESULT_FILE = os.path.join(base_dir, 'results/neat_results.json')
BEST_FILE = os.path.join(base_dir, 'models/neat_best.pkl')
CONFIG_FILE = os.path.join(base_dir, 'config/neat_config.txt')

def log_msg(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{ts}] {msg}"
    print(full_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(full_msg + "\n")

def eval_genome(genome, config, games=2):
    try:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        env = FlappyBirdEnv()
        total_fitness = 0
        
        for _ in range(games):
            obs, _ = env.reset()
            done = False
            frames = 0
            score = 0
            
            while not done and frames < 1000:
                action = 1 if net.activate(obs)[0] > 0.5 else 0
                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                frames += 1
                score = info.get('score', 0)
            
            fitness = score * 100 + frames
            total_fitness += fitness
        
        env.close()
        return total_fitness / games
    except:
        return 0.0

def eval_genomes(genomes, config):
    for gid, genome in genomes:
        genome.fitness = eval_genome(genome, config)

log_msg("=" * 70)
log_msg("NEAT TRAINING - BOT A (IMPROVED)")
log_msg("=" * 70)

if not os.path.exists(CONFIG_FILE):
    log_msg(f"ERROR: Config not found")
else:
    start = time.time()
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, CONFIG_FILE)
    config.pop_size = 100
    log_msg(f"Population: {config.pop_size}, Fitness: frames + score*100")
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    log_msg("Starting evolution (up to 30 gen or 58 min)...")
    
    winner = p.run(eval_genomes, 30)
    elapsed = time.time() - start
    
    log_msg(f"Completed in {elapsed:.1f}s, Best Fitness={winner.fitness:.0f}")
    
    with open(BEST_FILE, 'wb') as f:
        pickle.dump((winner, config), f)
    log_msg(f"Saved genome")
    
    log_msg("Final evaluation (10 episodes)...")
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    env = FlappyBirdEnv()
    scores = []
    frames_list = []
    
    for i in range(10):
        obs, _ = env.reset()
        done = False
        frames = 0
        while not done and frames < 1000:
            action = 1 if net.activate(obs)[0] > 0.5 else 0
            obs, _, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            frames += 1
        score = info.get('score', 0)
        scores.append(score)
        frames_list.append(frames)
        log_msg(f"  Ep {i+1}: Score={score}, Frames={frames}")
    
    env.close()
    scores = np.array(scores)
    frames_arr = np.array(frames_list)
    
    log_msg(f"RESULTS:")
    log_msg(f"  Scores: mean={scores.mean():.1f}, max={scores.max()}")
    log_msg(f"  Frames: mean={frames_arr.mean():.0f}, max={frames_arr.max()}")
    
    with open(RESULT_FILE, 'w') as f:
        json.dump({'scores': list(map(int, scores)), 'frames': list(map(int, frames_arr)),
                   'score_mean': float(scores.mean()), 'frames_mean': float(frames_arr.mean())}, f)
    log_msg("=" * 70)
