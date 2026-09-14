"""TianDao Seed (天道种子) — Local-first 5-node conservation kernel.
Law layer (allocate): a dead, auditable, training-free conservation flow.
State layer (x, gamma): living, local, and shaped only by *your* usage.
No cloud. No accounts. No telemetry. Binds 127.0.0.1 only.
"""
import json
import os

N = 5
NAME = ["Compute", "Data", "Task", "Memory", "Collab"]
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_state.json")


def allocate(x, gamma, need, a=1.0, b=0.6, dt=0.02, steps=200):
    """Law (dead structure, no thinking): 5-node conservation flow + zero-sum need drive.
    drive = need_g - mean(need_g): total attention budget == 1, need only redistributes.
    Σx == 1 at every single step (analytically); the final normalize is just numerical safety."""
    need_g = [need[i] * gamma[i] for i in range(N)]
    mean_g = sum(need_g) / N
    for _ in range(steps):
        nx = []
        for i in range(N):
            gen = a * (x[(i - 1) % N] * (1 - x[i]) - x[i] * (1 - x[(i + 1) % N]))
            inh = b * (x[(i + 2) % N] * (1 - x[i]) - x[i] * (1 - x[(i - 2) % N]))
            drive = need_g[i] - mean_g          # zero-sum: pushes flow toward need, ledger untouched
            nx.append(x[i] + dt * (gen + inh + drive))
        nx = [max(1e-9, v) for v in nx]        # boundary floor (AUDIT-acknowledged numerical crutch)
        x = nx
    s = sum(x)
    return [v / s for v in x]


def load():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH, encoding="utf-8"))
    return {"x": [.2] * 5, "g": [1.0] * 5}


def save(d):
    json.dump(d, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False)


NEED = {  # intent -> 5-dim need vector
    "code": [.8, .3, .9, .2, .1],
    "mem": [.2, .4, .2, .9, .1],
    "write": [.3, .7, .8, .3, .1],
    "collab": [.3, .3, .3, .3, .9],
}


def classify(text):
    """Minimal offline intent recognition: keyword match (EN + ZH). Rough on purpose."""
    t = text.lower()
    if any(k in t for k in ["remind", "birthday", "date", "remember", "记", "生日", "月", "号", "日", "健身"]):
        return "mem"
    if any(k in t for k in ["write", "novel", "article", "poem", "写", "小说", "文章", "诗"]):
        return "write"
    if any(k in t for k in ["collab", "together", "help", "协", "一起", "帮"]):
        return "collab"
    return "code"


def process_request(user_text):
    intent = classify(user_text)
    d = load()
    x = allocate(d["x"], d["g"], NEED.get(intent, [.4] * 5))
    idx = max(range(N), key=lambda i: x[i])      # awaken the hammer with the largest share
    d["g"][idx] = min(d["g"][idx] * 1.08 * 0.995, 8.0)  # Hebbian grow + TianDao forgetting + hard cap
    d["x"] = x
    save(d)
    return {
        "intent": intent,
        "alloc": [round(v, 2) for v in x],
        "gamma": [round(v, 2) for v in d["g"]],
        "awaken": NAME[idx],
    }


if __name__ == "__main__":
    for text in ["write a quicksort", "remember mom's birthday 3.5",
                 "write a rainy-night novel", "binary search", "gym every wednesday"]:
        r = process_request(text)
        print(f"Need[{r['intent']}] {text}")
        print(f"  Alloc={r['alloc']} Σ={round(sum(r['alloc']), 3)} → Awakened [{r['awaken']}]")
        print(f"  γ={r['gamma']} (deviated from [1,1,1,1,1], shaped by you)\n")
