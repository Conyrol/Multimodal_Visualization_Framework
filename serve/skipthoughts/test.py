import skipthoughts
model = skipthoughts.load_model()
encoder = skipthoughts.Encoder(model)

vectors = encoder.encode(["I don't konw"])
print len(vectors)
print vectors