import random
import difflib


class FarmMind:

    def __init__(self, knowledge_base):

        print("🌱 Starting FarmMind AI...")

        self.kb = knowledge_base
        self.index = []
        self.words = set()

        self.build_index()

        self.tips = [
            "Rotate crops to prevent pest buildup.",
            "Use organic compost to improve soil fertility.",
            "Inspect crops weekly for early pest detection.",
            "Water crops early morning or evening.",
            "Use resistant crop varieties when possible.",
            "Healthy soil leads to healthy crops.",
            "Avoid overwatering crops.",
            "Remove infected plants early to stop disease spread."
        ]

        print("✅ FarmMind ready. Knowledge entries:", len(self.index))

    # --------------------------------
    # Build search index
    # --------------------------------

    def build_index(self):

        for category, items in self.kb.items():

            if isinstance(items, dict):

                for crop, details in items.items():

                    if isinstance(details, dict):

                        for key, value in details.items():

                            if isinstance(value, list):

                                for item in value:

                                    text = f"{crop} {key} {item}".lower()

                                    self.index.append(text)

                                    for w in text.split():
                                        self.words.add(w)

    # --------------------------------
    # Fix misspelled words
    # --------------------------------

    def correct_words(self, question):

        corrected = []

        for w in question.split():

            match = difflib.get_close_matches(w, self.words, n=1, cutoff=0.7)

            if match:
                corrected.append(match[0])
            else:
                corrected.append(w)

        return " ".join(corrected)

    # --------------------------------
    # Search knowledge
    # --------------------------------

    def search(self, question):

        q = question.lower()

        results = []

        for entry in self.index:

            score = 0

            for word in q.split():

                if word in entry:
                    score += 1

            if score > 0:
                results.append((score, entry))

        results.sort(reverse=True)

        return [r[1] for r in results[:5]]

    # --------------------------------
    # Suggestions
    # --------------------------------

    def suggestions(self):

        return [
            "What pests attack maize?",
            "How to control aphids?",
            "Why are my leaves yellow?",
            "Common tomato diseases",
            "How to improve soil fertility?",
            "How to increase crop yield?"
        ]

    # --------------------------------
    # Main AI response
    # --------------------------------

    def answer(self, question):

        if not question:
            return "Please ask a farming question."

        q = question.lower()

        # Greetings
        if any(x in q for x in ["hi", "hello", "hey"]):
            return (
                "Hello! 👋 I am FarmMind 🌱\n\n"
                "I help farmers diagnose crop problems, pests, and diseases.\n\n"
                "Example questions:\n"
                "• maize problems\n"
                "• tomato diseases\n"
                "• pests affecting cabbage\n"
            )

        # Goodbye
        if any(x in q for x in ["bye", "goodbye", "see you"]):
            return "Goodbye! 🌾 Wishing you healthy crops and a great harvest."

        # About
        if "about" in q or "who are you" in q:
            return (
                "About FarmMind\n"
                "──────────────\n"
                "FarmMind is an agricultural AI assistant designed to help "
                "farmers identify crop diseases, pests, and farming problems.\n\n"
                "It uses a large farming knowledge base to provide useful "
                "agriculture advice."
            )

        # Fix spelling
        q = self.correct_words(q)

        # Search knowledge
        results = self.search(q)

        if results:

            response = "Possible Causes\n"
            response += "───────────────\n"

            for r in results:
                response += f"• {r.replace('_', '')}\n"

            response += "\nFarming Tip\n"
            response += "───────────\n"

            response += f"• {random.choice(self.tips)}\n"

            response += "\nNext Questions\n"
            response += "──────────────\n"

            for s in self.suggestions():
                response += f"• {s}\n"

            return response

        return (
            "I couldn't find that in my farming knowledge.\n"
            "Try asking about crops, pests, soil, or diseases."
        )

        # fix spelling
        q = self.correct_words(q)

        # search
        results = self.search(q)

        if results:

            response = "Here are some possible answers:\n\n"

            for i, r in enumerate(results, 1):

                response += f"{i}. {r}\n"

            response += "\n🌿 Farming Tip:\n"
            response += random.choice(self.tips)

            response += "\n\nYou may also ask:\n"

            for s in self.suggestions():
                response += f"• {s}\n"

            return response

        return (
            "I couldn't find that yet in my farming knowledge.\n"
            "Try asking about crops, pests, diseases or soil."
        )


# Flask helper
def farmmind_respond(question):

    from knowledge_base import agriculture_knowledge

    brain = FarmMind(agriculture_knowledge)

    return brain.answer(question)
