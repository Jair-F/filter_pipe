from src.pipeline.pipeline import Pipeline


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
    print(pipeline.is_valid_filter(" lpass(n=999999) "))