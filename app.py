import html
import random
import secrets
import string
import time
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="またあとワニさん", page_icon="🐊", layout="centered")
ASSETS = Path(__file__).parent / "assets"

NATURAL_NAMES = [
    "すみれ", "なずな", "れんげ", "つばき", "あざみ", "ききょう", "すずらん", "あやめ", "りんどう", "ひなげし",
    "つゆくさ", "たんぽぽ", "よもぎ", "すすき", "つくし", "くるみ", "かえで", "もみじ", "若葉", "青葉",
    "若草", "さくら", "なのはな", "ミモザ", "クローバー", "ラベンダー", "ネモフィラ", "オリーブ",
    "つばめ", "ひばり", "すずめ", "こまどり", "かわせみ", "めじろ", "うぐいす", "ちどり", "かもめ", "ふくろう",
    "つぐみ", "せきれい", "ヤマガラ", "カナリア",
    "すばる", "三日月", "満月", "月影", "月夜", "星空", "星影", "流れ星", "天の川", "夜空", "青空", "夕空",
    "朝焼け", "夕焼け", "夜明け", "月明かり", "星明かり", "ひかり",
    "こもれび", "そよ風", "春風", "秋風", "潮風", "ゆうなぎ", "あさなぎ", "しぐれ", "小雨", "霧雨",
    "夕立", "朝露", "かすみ", "おぼろ", "夕雲", "虹",
    "せせらぎ", "さざなみ", "しおさい", "なぎさ", "波音", "水音", "泉", "小川", "しずく", "雨粒", "みなも", "なぎ",
    "こだま", "こだち", "こみち", "野原", "砂浜", "木陰", "陽だまり", "ひなた", "夕暮れ", "新緑", "初雪", "小春",
]


def make_search_id():
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(5))


st.markdown(
    """
<style>
:root{--cream:#fbf7ed;--paper:#fffdf7;--green:#667a3c;--dark:#4b3a2d;--yellow:#f1c85b;--line:#e5ddca;--soft:#f2ecdc}
.stApp{background:var(--cream);color:var(--dark)}
.block-container{max-width:720px;padding:1rem 1rem 6rem}
h1,h2,h3,p,div,button,input,textarea{font-family:"Hiragino Maru Gothic ProN","Yu Gothic",sans-serif}
[data-testid="stHeader"]{background:transparent}
.hero{background:var(--paper);border:1px solid var(--line);border-radius:24px;padding:14px 18px;text-align:center;box-shadow:0 5px 18px #6b5a3a10}
.hero img{max-width:390px;width:100%;border-radius:18px}.hero p{margin:.25rem;color:#766a59}.concept{font-size:1.05rem;font-weight:700;color:#53662f;margin-top:8px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:14px 16px;margin:10px 0}
.name{font-weight:700;color:var(--dark)}.meta{font-size:.78rem;color:#8a806f}.body{line-height:1.8;margin:.55rem 0}
.pill{display:inline-block;background:#eef1df;color:#58683b;padding:4px 10px;border-radius:999px;font-size:.82rem;margin:2px}
.reply{background:#fff4ce;border:1px solid #ebd88e;border-radius:14px;padding:10px 12px;color:#6c5831}
.mine{border-left:5px solid var(--green)}
.letter{border:1px solid #ded3bd;border-radius:18px;padding:14px;margin:10px 0;max-width:88%}
.letter.theirs{background:#fffdf8;margin-right:12%}
.letter.mine{background:#eef3df;border-color:#cbd6a9;margin-left:12%}
.direction{font-size:.76rem;font-weight:700;color:#6f7658;margin-bottom:5px}
.stButton>button,.stFormSubmitButton>button{border-radius:999px;border:0;background:var(--green);color:white;font-weight:700;min-height:42px}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#53662f;color:white}
[data-testid="stBottomBlockContainer"]{background:var(--cream)}
.small{font-size:.82rem;color:#817765}.center{text-align:center}
</style>
""",
    unsafe_allow_html=True,
)


def init_state():
    defaults = {
        "page": "新しい日記",
        "display_name": "",
        "proposed_name": random.choice(NATURAL_NAMES),
        "previous_names": [],
        "onboarding_complete": False,
        "user_uuid": str(uuid.uuid4()),
        "search_id": make_search_id(),
        "icon": "116748_0(1).jpg",
        "bio": "",
        "likes": ["散歩", "本", "喫茶店"],
        "letter_note": "返事はゆっくりでも大丈夫です。",
        "search_visible": True,
        "mute_words": ["政治"],
        "muted_people": set(),
        "blocked_people": set(),
        "reaction_log": [],
        "reply_status": {},
        "sent_letters": [],
        "thread_names": {"p_sumire": "すみれ", "p_komorebi_a": "こもれび"},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if "profile_text_v2" not in st.session_state:
        if st.session_state.bio == "散歩と本と、静かな夜が好きです。":
            st.session_state.bio = ""
        st.session_state.profile_text_v2 = True
    if st.session_state.display_name == "こもれび星":
        st.session_state.display_name = ""
        st.session_state.onboarding_complete = False

    if "diaries" not in st.session_state:
        st.session_state.diaries = [
            {"id": 1, "author_id": "p_sumire", "name": "すみれ", "icon": "116744_0(1).jpg", "when": "今日 9:10", "text": "朝の散歩で白い花を見つけました。名前は分からないけれど、風に揺れてきれいでした。", "photo": "116744_0(1).jpg", "scope": "みんな", "reaction": None},
            {"id": 2, "author_id": "p_komorebi_a", "name": "こもれび", "icon": "116740_0(1).jpg", "when": "昨日 22:40", "text": "読みかけの本を、今夜やっと読み終えました。少し余韻にひたっています。", "photo": "116740_0(1).jpg", "scope": "みんな", "reaction": None},
            {"id": 3, "author_id": "p_asagumo", "name": "あさぐも", "icon": "116739_0(1).jpg", "when": "昨日 7:20", "text": "雲の形が大きな船みたいでした。", "photo": "116739_0(1).jpg", "scope": "みんな", "reaction": None},
        ]
    if "threads" not in st.session_state:
        st.session_state.threads = {
            "p_sumire": [
                ("them", "この前教えてくれた本、読み始めました。", "昨日 20:12"),
                ("me", "うれしい。急がず読んでみてください。", "昨日 21:03"),
                ("them", "ありがとう。また感想を送ります。", "今日 8:42"),
            ],
            "p_komorebi_a": [("them", "週末、あの喫茶店に行きました。", "月曜 18:20")],
        }


init_state()


def onboarding(show_logo=True):
    logo = ASSETS / "02_______________________1024(1).png"
    if show_logo and logo.exists():
        left, middle, right = st.columns([1, 3, 1])
        with middle:
            st.image(str(logo), use_container_width=True)
    st.markdown("<div class='center'><h2>あなたに、こんな名前はいかが？</h2></div>", unsafe_allow_html=True)
    if not st.session_state.get("custom_name_mode", False):
        st.markdown(f"<div class='hero'><h1>{safe(st.session_state.proposed_name)}</h1></div>", unsafe_allow_html=True)
        if st.button("この名前にする", use_container_width=True, type="primary"):
            st.session_state.display_name = st.session_state.proposed_name
            st.session_state.onboarding_complete = True
            st.rerun()
        if st.button("もうひとつ見る", use_container_width=True):
            history = (st.session_state.previous_names + [st.session_state.proposed_name])[-12:]
            choices = [name for name in NATURAL_NAMES if name not in history]
            st.session_state.previous_names = history
            st.session_state.proposed_name = random.choice(choices or NATURAL_NAMES)
            st.rerun()
        if st.button("自分でつける", use_container_width=True):
            st.session_state.custom_name_mode = True
            st.rerun()
    else:
        custom = st.text_input("つけたい名前", placeholder="呼ばれたい名前を入力してください")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("この名前にする", use_container_width=True, disabled=not custom.strip()):
                st.session_state.display_name = custom.strip()
                st.session_state.onboarding_complete = True
                st.session_state.custom_name_mode = False
                st.rerun()
        with c2:
            if st.button("名前の提案に戻る", use_container_width=True):
                st.session_state.custom_name_mode = False
                st.rerun()
    st.caption("表示名はほかの人と同じでも大丈夫です。あとから変更できます。")


def safe(value):
    return html.escape(str(value)).replace("\n", "<br>")


def icon_path(filename):
    path = ASSETS / filename
    return str(path) if path.exists() else None


def header():
    logo = ASSETS / "02_______________________1024(1).png"
    if logo.exists():
        st.markdown('<div class="hero">', unsafe_allow_html=True)
        st.image(str(logo), use_container_width=True)
        st.markdown("<div class='concept'>人との距離も、ことばの速さも、自分で決める。</div><p>「あとで」ができる。心、軽やか。<br>つながることを、急がない。</p></div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero"><h1>またあとワニさん</h1><p>「あとで」ができる。心、軽やか。</p></div>', unsafe_allow_html=True)


def navigate():
    items = ["新しい日記", "みんなの日記", "おてがみ", "人をさがす", "ワニ園だより", "わたし"]
    st.session_state.page = st.radio("メニュー", items, horizontal=True, label_visibility="collapsed", key="nav")


def diary_card(post):
    if post.get("author_id") in st.session_state.muted_people or post.get("author_id") in st.session_state.blocked_people:
        return
    lower = post["text"].lower()
    if any(w.strip().lower() in lower for w in st.session_state.mute_words if w.strip()):
        return
    cols = st.columns([1, 5])
    with cols[0]:
        if icon_path(post["icon"]):
            st.image(icon_path(post["icon"]), use_container_width=True)
    with cols[1]:
        st.markdown(f'<div class="name">{safe(post["name"])}</div><div class="meta">{safe(post["when"])}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="body">{safe(post["text"])}</div>', unsafe_allow_html=True)
    if post.get("photo") and icon_path(post["photo"]):
        st.image(icon_path(post["photo"]), use_container_width=True)
    labels = ["いいね", "わかる", "おつかれさま", "すてき"]
    picked = st.segmented_control("リアクション", labels, key=f"react_{post['id']}", label_visibility="collapsed")
    if picked and picked != post.get("reaction"):
        post["reaction"] = picked
        st.session_state.reaction_log.append((post["name"], picked, post["id"]))
        st.toast(f"「{picked}」を届けました。数は公開されません。")


def new_diary():
    st.subheader("新しい日記")
    st.caption("一言でも、写真だけでも。書きたい長さでどうぞ。")
    with st.form("diary_form", clear_on_submit=True):
        text = st.text_area("今日のこと", placeholder="いま残しておきたいことはありますか？", height=150)
        photo = st.file_uploader("写真（なくても大丈夫です）", type=["jpg", "jpeg", "png"])
        scope = st.radio("公開範囲", ["みんな", "自分だけ"], horizontal=True)
        submitted = st.form_submit_button("日記をしまう")
    if submitted:
        if not st.session_state.display_name.strip():
            st.warning("日記を公開する前に、「わたし」で名前を決めてください。")
        elif not text.strip() and photo is None:
            st.warning("文章か写真のどちらかを入れてください。")
        else:
            st.session_state.diaries.insert(0, {"id": int(time.time()*1000), "author_id": st.session_state.user_uuid, "name": st.session_state.display_name, "icon": st.session_state.icon, "when": "たった今", "text": text or "（写真の日記）", "photo": None, "scope": scope, "reaction": None})
            st.success("日記をしまいました。" if scope == "自分だけ" else "日記を公開しました。")
    st.markdown("### わたしの最近の日記")
    mine = [x for x in st.session_state.diaries if x["name"] == st.session_state.display_name]
    if not mine:
        st.info("まだ日記はありません。")
    for p in mine[:3]:
        st.markdown(f'<div class="card mine"><span class="pill">{safe(p["scope"])}</span><div class="body">{safe(p["text"])}</div><div class="meta">{safe(p["when"])}</div></div>', unsafe_allow_html=True)


def timeline():
    st.subheader("みんなの日記")
    st.caption("おすすめ順ではなく、新しい順に並んでいます。")
    shown = 0
    for post in st.session_state.diaries:
        if post["scope"] != "みんな" or post["name"] == st.session_state.display_name:
            continue
        before = shown
        text = post["text"].lower()
        if post.get("author_id") not in st.session_state.muted_people | st.session_state.blocked_people and not any(w.lower() in text for w in st.session_state.mute_words if w):
            shown += 1
        if before != shown:
            with st.container(border=True):
                diary_card(post)
    if shown == 0:
        st.info("表示できる新しい日記はありません。見ないキーワードの設定も確認できます。")


STATUS = {
    "まだ決めない": "届いています",
    "いま返す": "いま返すみたい",
    "ちょっとあと": "ちょっとあと（20分くらい）に返すみたい",
    "あとで": "あとで（数時間くらい）返すみたい",
    "明日返す": "明日くらいに返すみたい",
    "少し考えたい": "少し考えてから返すみたい",
}


def letters():
    st.subheader("おてがみ")
    names = [n for n in st.session_state.threads if n not in st.session_state.blocked_people]
    if not names:
        st.info("まだ、やりとりはありません。")
        return
    person = st.selectbox("やりとりする人", names, format_func=lambda person_id: st.session_state.thread_names.get(person_id, person_id))
    person_name = st.session_state.thread_names.get(person, person)
    current = st.session_state.reply_status.get(person, "まだ決めない")
    st.markdown(f'<div class="reply">あなたの予定：{safe(STATUS[current])}</div>', unsafe_allow_html=True)
    choice = st.selectbox("返信の予定を伝える", list(STATUS), index=list(STATUS).index(current))
    if choice != current:
        st.session_state.reply_status[person] = choice
        st.toast("返信予定をやわらかく伝えました。あとから変更できます。")
    st.markdown("#### やりとり")
    for who, body, when in st.session_state.threads[person]:
        if who == "them":
            css = "letter theirs"
            direction = f"{person_name}さんから届いた手紙"
        else:
            css = "letter mine"
            direction = "あなたが送った手紙"
        st.markdown(f'<div class="{css}"><div class="direction">{safe(direction)}</div><div class="body">{safe(body)}</div><div class="meta">{safe(when)}</div></div>', unsafe_allow_html=True)
    with st.form("letter_form", clear_on_submit=True):
        body = st.text_area("手紙を書く", placeholder="急がず、伝えたい言葉をどうぞ。", height=120)
        sent = st.form_submit_button("ワニさんに手紙をあずける")
    if sent and body.strip():
        holder = st.empty()
        holder.markdown('<div class="card center">✉️　🐊<br><span class="small">ワニさんが手紙を背中に乗せました</span></div>', unsafe_allow_html=True)
        time.sleep(.45)
        holder.markdown('<div class="card center">　　🐊💨<br><span class="small">てちてち……</span></div>', unsafe_allow_html=True)
        time.sleep(.45)
        st.session_state.threads[person].append(("me", body.strip(), datetime.now().strftime("今日 %H:%M")))
        st.session_state.reply_status[person] = "まだ決めない"
        holder.empty()
        st.success("手紙を届けました。")
        time.sleep(.2)
        st.rerun()


PEOPLE = [
    {"uid": "p_sumire", "search_id": "s3m8a", "name": "すみれ", "icon": "116744_0(1).jpg", "bio": "花と料理が好きです。", "note": "お返事は夜になることが多いです。", "likes": "花、料理"},
    {"uid": "p_komorebi_a", "search_id": "k7m2p", "name": "こもれび", "icon": "116740_0(1).jpg", "bio": "本と散歩が好きです。", "note": "ゆっくり考えて返します。", "likes": "本、散歩"},
    {"uid": "p_komorebi_b", "search_id": "f4n9q", "name": "こもれび", "icon": "116747_0(1).jpg", "bio": "静かな喫茶店が好きです。", "note": "短い手紙もうれしいです。", "likes": "喫茶店、小鳥"},
    {"uid": "p_asagumo", "search_id": "a2g6w", "name": "あさぐも", "icon": "116739_0(1).jpg", "bio": "空の写真をよく撮ります。", "note": "あとで、ええんやで。", "likes": "空、写真"},
]


def search_people():
    st.subheader("名前で人をさがす")
    st.caption("おすすめは表示しません。話してみたい人を自分で探せます。")
    q = st.text_input("名前", placeholder="例：すみれ")
    if not q:
        st.info("名前の一部を入力してください。")
        return
    query = q.strip().lower()
    results = [p for p in PEOPLE if (query in p["name"].lower() or query == p["search_id"]) and p["uid"] not in st.session_state.blocked_people]
    if not results:
        st.info("見つかりませんでした。")
    for person in results:
        name, icon, bio, note = person["name"], person["icon"], person["bio"], person["note"]
        with st.container(border=True):
            c1, c2 = st.columns([1, 4])
            with c1: st.image(icon_path(icon), use_container_width=True)
            with c2:
                st.markdown(f"**{name}**  \n{bio}  \n<span class='small'>好きなもの：{person['likes']}<br>お手紙について：{note}</span>", unsafe_allow_html=True)
            if st.button("話しかける", key=f"talk_{person['uid']}"):
                st.session_state.threads.setdefault(person["uid"], [])
                st.session_state.thread_names[person["uid"]] = name
                st.session_state.page = "おてがみ"
                st.toast(f"{name}さんとの、おてがみを開きました。")


def profile():
    st.subheader("わたし")
    tabs = st.tabs(["プロフィール", "見るもの・距離", "リアクション"])
    with tabs[0]:
        if not st.session_state.display_name.strip():
            st.info("名前は、ここでゆっくり決められます。")
            onboarding(show_logo=False)
            st.markdown("---")
        icon_names = {
            "116739_0(1).jpg": "青空と雲",
            "116740_0(1).jpg": "月夜",
            "116741_0(1).jpg": "星空",
            "116742_0(1).jpg": "雨粒",
            "116743_0(1).jpg": "海辺の真珠",
            "116744_0(1).jpg": "白い花",
            "116745_0(1).jpg": "朝の太陽",
            "116746_0(1).jpg": "雪山",
            "116747_0(1).jpg": "小鳥",
            "116748_0(1).jpg": "若葉",
        }
        icon_files = list(icon_names)
        with st.form("profile_form"):
            name = st.text_input("名前", st.session_state.display_name)
            icon = st.selectbox("アイコン", icon_files, index=icon_files.index(st.session_state.icon) if st.session_state.icon in icon_files else 0, format_func=lambda filename: icon_names[filename])
            if icon_path(icon): st.image(icon_path(icon), width=120)
            bio = st.text_area("ひとこと", st.session_state.bio, placeholder="すきなことをひとことどうぞ")
            likes = st.text_input("好きなもの（最大5個・読点区切り）", "、".join(st.session_state.likes))
            note = st.text_area("お手紙についての一言", st.session_state.letter_note)
            visible = st.toggle("名前検索に表示する", st.session_state.search_visible)
            save = st.form_submit_button("プロフィールを保存")
        if save:
            st.session_state.display_name = name.strip() or st.session_state.display_name
            st.session_state.icon = icon
            st.session_state.bio = bio
            st.session_state.likes = [x.strip() for x in likes.replace(",", "、").split("、") if x.strip()][:5]
            st.session_state.letter_note = note
            st.session_state.search_visible = visible
            st.success("保存しました。")
    with tabs[1]:
        words = st.text_area("見ないキーワード（1行に1つ）", "\n".join(st.session_state.mute_words), help="その言葉を含む公開日記を、あなただけに表示しません。投稿者には通知されません。")
        if st.button("見ないキーワードを保存"):
            st.session_state.mute_words = [x.strip() for x in words.splitlines() if x.strip()]
            st.success("保存しました。")
        st.markdown("#### ミュート・ブロック")
        target = st.selectbox("相手", [p["uid"] for p in PEOPLE], format_func=lambda uid: next(p["name"] for p in PEOPLE if p["uid"] == uid))
        c1, c2 = st.columns(2)
        with c1:
            muted = target in st.session_state.muted_people
            if st.button("ミュートを解除" if muted else "静かにミュート", key="mute"):
                (st.session_state.muted_people.discard if muted else st.session_state.muted_people.add)(target)
                st.rerun()
        with c2:
            blocked = target in st.session_state.blocked_people
            if st.button("ブロックを解除" if blocked else "ブロック", key="block"):
                (st.session_state.blocked_people.discard if blocked else st.session_state.blocked_people.add)(target)
                st.rerun()
        st.caption("ミュートやブロックは相手に通知されません。通報は動作確認版では送信されません。")
    with tabs[2]:
        st.caption("受け取ったリアクションは投稿者本人だけが確認できます。公開数やランキングはありません。")
        st.info("動作確認版では、自分の日記への受信例をここに表示する予定です。")


def garden_news():
    st.subheader("ワニ園だより")
    st.caption("またあとワニ園 園長が、アプリのことや考えていることを、ぽつぽつ書きます。")
    category = st.selectbox("読みたい棚", ["すべて", "園長室から", "飼育日誌", "園内のおしらせ", "ワニの観察記録", "考え中です"])
    articles = [
        ("園長室から", "人との距離も、ことばの速さも、自分で決める。", "このワニ園は、ゆっくりすることを押しつける場所ではありません。今返すことも、あとで返すことも、少し離れることも、自分で選べる場所にしたいと考えています。"),
        ("園長室から", "なぜ、既読を置かないのか", "読んだことが、そのまま返事の催促にならないように。代わりに、返せそうな頃をやわらかく伝えられる形を育てています。"),
        ("園長室から", "おすすめ機能を作らない理由", "何を見るかまでアプリが決めず、自分で新しい日記を見たり、名前から人を探したりできるようにしています。"),
        ("飼育日誌", "動作確認版ができました", "日記、おてがみ、返信予定、名前検索、見ないキーワードなど、ワニ園の基本的な過ごし方を試せるようになりました。"),
        ("ワニの観察記録", "手を背中にのせるワニ", "手紙は口にくわえず、ずんぐりした背中にのせて、てちてち運びます。急がないけれど、ちゃんと届けます。"),
        ("考え中です", "木の実のこと", "いつの間にか少し貯まり、自分の居場所を好みに整えられる小さなお楽しみを考えています。ノルマや連続記録にはしません。"),
    ]
    visible = articles if category == "すべて" else [a for a in articles if a[0] == category]
    for cat, title, body in visible:
        with st.expander(title):
            st.markdown(f'<span class="pill">{safe(cat)}</span><div class="body">{safe(body)}</div><div class="meta">またあとワニ園　園長</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 木の実について 🌰")
    st.caption("将来機能・現在はまだ貯まりません")
    st.markdown("""
    普通にワニ園で過ごしていたら、いつの間にか少し貯まっているお楽しみです。
    将来はワニさんの色、便箋、封筒、壁紙など、自分の居場所を整えるために使えます。
    所持数やランキングは他人に公開せず、ミッションやストリークも設けません。
    """)
    st.info("園長へのお手紙は将来追加予定です。公開コメント欄は設けません。")


header()
navigate()
page = st.session_state.page
if page == "新しい日記": new_diary()
elif page == "みんなの日記": timeline()
elif page == "おてがみ": letters()
elif page == "人をさがす": search_people()
elif page == "ワニ園だより": garden_news()
else: profile()

st.markdown('<div class="center small" style="margin-top:32px">あとで、ええんやで 🐊</div>', unsafe_allow_html=True)
