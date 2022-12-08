from Coach import Coach
import os

if __name__=="__main__":
    if not os.path.exists("./Tables"):
        os.mkdir("./Tables")
    c = Coach()
    folder = "./previous_models/previous_model_11.pth.tar"
    if os.path.exists(folder):
        print("Load trainExamples from file")
        c.loadTrainExamples()
    else:
        print("use new trainExamples")
    c.learn()
