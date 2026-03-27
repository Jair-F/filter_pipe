from src.pipeline.pipeline import Pipeline


if __name__ == "__main__":
    pipeline = Pipeline("mavg(n=10)|lpass(alpha=0.2)")
    pipeline.run()
    print(pipeline.is_valid_filter(" lpass(n=999999) "))