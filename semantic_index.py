from sentence_transformers import SentenceTransformer, util


class SemanticIndex:

    def __init__(self, knowledge_base):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.sentences = []
        self.answers = []

        for category, topics in knowledge_base.items():

            if isinstance(topics, dict):

                for topic, info in topics.items():

                    if isinstance(info, dict):

                        for key, value in info.items():

                            sentence = f"{topic} {key}"
                            answer = f"{topic.title()} - {key}: {value}"

                            self.sentences.append(sentence)
                            self.answers.append(answer)

                    else:
                        self.sentences.append(topic)
                        self.answers.append(info)

        # create embeddings
        if self.sentences:
            self.embeddings = self.model.encode(self.sentences)
        else:
            self.embeddings = []

    def search(self, query):

        if not query.strip():
            return None

        if not self.embeddings:
            return None

        q_embed = self.model.encode(query)

        scores = util.cos_sim(q_embed, self.embeddings)

        best_index = scores.argmax()

        return self.answers[best_index]
