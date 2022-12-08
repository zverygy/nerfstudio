"""
Process the Mipnerf360 dataset.
"""

from nerfstudio.utils.scripts import run_command

# # split = ["bicycle", "flowers", "garden", "stump", "treehill", "room", "counter", "kitchen", "bonsai"]
# splits = ["bicycle", "garden", "stump", "room", "counter", "kitchen", "bonsai"]


# # for processing data

# for split in splits:
#     print(f"Processing {split}...")
#     working_dir = "/home/ethanweber/nerfactory/data/_prep/images/mipnerf360"
#     cmd = f"ns-process-data images --data {working_dir}/{split}/images --output-dir {working_dir}/processed/{split}/"
#     output = run_command(cmd, verbose=True)

# for training

# 1/8 of input images used in the paper = 0.125 -> 1 - this = 0.875
# ns-train nerfacto --vis wandb --data data/nerfstudio/garden nerfstudio-data --downscale-factor 1 --train-split-percentage 0.875
# X turn off pose optimization
# turn off appearance optimization
# increase hash map size. max_res 2048
# ns-train nerfacto --vis wandb --data data/_prep/images/mipnerf360/processed/garden --pipeline.datamanager.camera-optimizer.mode off --trainer.steps-per-eval-all-images 5000 nerfstudio-data --downscale-factor 4


# mipnerf 360 experiments

splits = ["bicycle", "garden", "stump", "room", "counter", "kitchen", "bonsai"]  # 7 splits
gpus = [0, 1, 3, 4, 5, 6, 7]

commands = []
for split, gpu in zip(splits, gpus):
    wandb_name = f"mipnerf360-{split}"
    command = " ".join(
        (
            f"CUDA_VISIBLE_DEVICES={gpu}",
            "ns-train nerfacto",
            "--vis wandb",
            f"--wandb-name {wandb_name}",
            f"--data data/_prep/images/mipnerf360/processed/{split}",
            "--pipeline.datamanager.camera-optimizer.mode off",
            "--trainer.steps-per-eval-all-images 5000",
            "--trainer.max-num-iterations 250000",
            "--pipeline.model.use_appearance_embedding False",
            "nerfstudio-data",
            "--downscale-factor 4",
        )
    )
    print(command)
    commands.append(command)
# import subprocess
# import sys
# def f(cmd):
#     out = subprocess.run(cmd, capture_output=False, shell=True, check=False)
#     if out.returncode != 0:
#         print(f"Error running command: {cmd}")
#         sys.exit(1)
#     if out.stdout is not None:
#         return out.stdout.decode("utf-8")

# from multiprocessing import Pool
# with Pool() as p:
#     print(p.map(f, commands))