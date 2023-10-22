
def split_into_buckets(phrase, n):
    if ' ' not in phrase and len(phrase.strip()) > n:
            return []
    if len(phrase.strip()) <= n:
        return [phrase.strip()]

    words = phrase.strip().split(' ')
    word_count = [len(word) + i for i, word in enumerate(words)]
    idx = len([sum(word_count[:i+1]) for i in range(len(word_count)) if sum(word_count[:i+1]) <= n]) - 1

    if idx == -1:
        return []
    return [' '.join(words[:idx+1])] + split_into_buckets(' '.join(words[idx+1:]), n)

print(
    split_into_buckets("she sells sea shells by the sea", 2)
)
