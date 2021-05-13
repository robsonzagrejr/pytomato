def make_follow(first, gramatica):
    follow = dict()
    keys = list(gramatica.keys())
    for n_terminal in keys:
        follow[n_terminal] = set()

    follow["S"] = set(["$"])
    for item1 in gramatica.items():
        for item2 in item1[1]:
            for idx, terminal in enumerate(item2):
                try:
                    next_item = item2[idx+1]
                    if keys.count(terminal) >= 1:
                        if keys.count(next_item) >= 1:
                            follow[terminal].update(first[next_item])
                        else:
                            follow[terminal].add(next_item)
                except Exception:
                    pass
                
    for item1 in gramatica.items():
        for item2 in item1[1]:
            terminal = item2[-1]
            if keys.count(terminal) >= 1:
                follow[terminal].update(list(follow[item1[0]]))
        

    for item in follow.keys():
        follow[item].discard("&")
        follow[item] = list(follow[item])

    return follow

if __name__ == '__main__':
    tes =  { "S": ["aAA", "bB", "cS"], "A": ["aS", "bC&", "b", "cA"], "B": ["aCc", "a", "bS", "cBc"], "C": ["aB", "bA", "cC", "c"] }
    first = {"S": ["a", "b", "c"], "A": ["a", "b"], "B": ["a"], "C": ["c"]}
    print(make_follow(first, tes))
