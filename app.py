from flask import Flask, render_template_string

app = Flask(__name__)

SUPABASE_URL = "https://riolotorwqffbiekspkc.supabase.co"
SUPABASE_KEY = "sb_publishable_nnGkSCQSlX1HnY-lTo1zvQ_-f5iCxVC"

PAGE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MACAVITY YHE</title>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

<style>
*{box-sizing:border-box}
body{
    margin:0;
    background:#05070a;
    color:#fff;
    font-family:Arial,sans-serif
}
.app{
    max-width:650px;
    min-height:100vh;
    margin:auto;
    background:#0c1016
}
header{
    height:65px;
    padding:0 18px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    border-bottom:1px solid #252b35
}
.logo{
    font-size:21px;
    font-weight:bold;
    letter-spacing:2px
}
.card{
    margin:16px;
    padding:18px;
    border-radius:18px;
    background:#141922;
    border:1px solid #282f3a
}
.title{
    font-size:19px;
    font-weight:bold;
    margin-bottom:14px
}
input{
    width:100%;
    padding:14px;
    margin:6px 0;
    border-radius:12px;
    border:1px solid #343c49;
    background:#080b10;
    color:white;
    outline:none
}
button{
    border:0;
    cursor:pointer;
    font-weight:bold
}
.primary{
    width:100%;
    padding:14px;
    margin-top:8px;
    border-radius:12px;
    background:#fff;
    color:#000
}
.secondary{
    padding:10px 14px;
    border-radius:10px;
    background:#242b37;
    color:white
}
.tabs{
    display:flex;
    gap:7px;
    padding:12px 16px
}
.tabs button{
    flex:1;
    padding:12px;
    border-radius:10px;
    background:#1a202a;
    color:#aaa
}
.tabs button.active{
    background:#fff;
    color:#000
}
.user{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:13px;
    margin:8px 0;
    border-radius:13px;
    background:#1a202a
}
.small{
    color:#909aaa;
    font-size:13px;
    margin-top:4px
}
.hidden{
    display:none!important
}
.chat{
    height:72vh;
    display:flex;
    flex-direction:column
}
.messages{
    flex:1;
    overflow-y:auto;
    padding:15px 0
}
.message{
    width:max-content;
    max-width:80%;
    padding:10px 13px;
    margin:7px 0;
    border-radius:16px;
    background:#202733;
    word-break:break-word
}
.message.mine{
    margin-left:auto;
    background:#fff;
    color:#000
}
.send{
    display:flex;
    gap:7px;
    border-top:1px solid #282f39;
    padding-top:10px
}
.send input{
    margin:0
}
.empty{
    color:#8993a3;
    text-align:center;
    padding:15px
}
</style>
</head>

<body>

<div class="app">

<header>
    <div class="logo">MACAVITY YHE</div>
    <button id="logout" class="secondary hidden"
            onclick="logout()">Logout</button>
</header>


<!-- AUTH -->

<section id="auth">

<div class="card">
    <div class="title">Create Account</div>

    <input id="name" placeholder="Your name">

    <input id="username" placeholder="@username">

    <input id="email" type="email" placeholder="Email">

    <input id="password" type="password" placeholder="Password">

    <button class="primary" onclick="signup()">
        CREATE ACCOUNT
    </button>
</div>


<div class="card">
    <div class="title">Login</div>

    <input id="lemail" type="email" placeholder="Email">

    <input id="lpassword" type="password" placeholder="Password">

    <button class="primary" onclick="login()">
        LOGIN
    </button>
</div>

</section>


<!-- APP -->

<section id="app" class="hidden">

<div class="tabs">

<button id="peopleTab"
        class="active"
        onclick="page('people')">
People
</button>

<button onclick="page('groups')">
Groups
</button>

<button onclick="page('profile')">
Profile
</button>

</div>


<!-- PEOPLE -->

<div id="people">

<div class="card">

<div class="title">Find People</div>

<input id="search"
       placeholder="Search username..."
       oninput="findUsers()">

<div id="users"></div>

</div>

</div>


<!-- GROUPS -->

<div id="groups" class="hidden">

<div class="card">

<div class="title">Create Group</div>

<input id="groupName"
       placeholder="Group name">

<button class="primary"
        onclick="createGroup()">
CREATE GROUP
</button>

</div>

<div class="card">

<div class="title">My Groups</div>

<div id="groupList"></div>

</div>

</div>


<!-- PROFILE -->

<div id="profile" class="hidden">

<div class="card">

<div class="title">My Profile</div>

<div id="profileData"></div>

<input id="pname"
       placeholder="Display name">

<input id="pbio"
       placeholder="Bio">

<button class="primary"
        onclick="saveProfile()">
SAVE PROFILE
</button>

</div>

</div>


<!-- CHAT -->

<div id="chat" class="hidden">

<div class="card chat">

<div>
<button class="secondary"
        onclick="closeChat()">
← Back
</button>

<span id="chatName"
      style="margin-left:10px;font-weight:bold">
</span>
</div>

<div id="messages"
     class="messages"></div>

<div class="send">

<input id="text"
       placeholder="Write a message..."
       onkeydown="if(event.key==='Enter')send()">

<button class="secondary"
        onclick="send()">
Send
</button>

</div>

</div>

</div>

</section>

</div>


<script>

const db = window.supabase.createClient(
    "{{ url }}",
    "{{ key }}"
);

let me = null;
let currentChat = null;
let realtime = null;


/* START */

window.onload = async function(){

    const r = await db.auth.getSession();

    if(r.data.session){

        me = r.data.session.user;

        startApp();
    }
};


/* SIGNUP */

async function signup(){

    const name =
        document.getElementById("name").value.trim();

    let username =
        document.getElementById("username")
        .value.trim()
        .toLowerCase()
        .replace("@","");

    const email =
        document.getElementById("email").value.trim();

    const password =
        document.getElementById("password").value;

    if(!name || !username || !email || !password){

        alert("Sab fields bharo.");
        return;
    }

    if(!/^[a-z0-9_]{3,20}$/.test(username)){

        alert(
            "Username 3-20 characters ka hona chahiye."
        );
        return;
    }

    if(password.length < 6){

        alert("Password minimum 6 characters ka rakho.");
        return;
    }

    const r = await db.auth.signUp({

        email:email,
        password:password,

        options:{
            data:{
                username:username,
                display_name:name
            }
        }
    });

    if(r.error){

        alert(r.error.message);
        return;
    }

    if(r.data.user){

        await db
        .from("profiles")
        .update({
            username:username,
            display_name:name
        })
        .eq("id",r.data.user.id);
    }

    alert(
        "Account ban gaya. " +
        "Agar email verification aaye to verify karo."
    );
}


/* LOGIN */

async function login(){

    const email =
        document.getElementById("lemail").value.trim();

    const password =
        document.getElementById("lpassword").value;

    const r = await db.auth.signInWithPassword({

        email:email,
        password:password
    });

    if(r.error){

        alert(r.error.message);
        return;
    }

    me = r.data.user;

    startApp();
}


/* APP */

function startApp(){

    document.getElementById("auth")
        .classList.add("hidden");

    document.getElementById("app")
        .classList.remove("hidden");

    document.getElementById("logout")
        .classList.remove("hidden");

    page("people");
    findUsers();
}


/* LOGOUT */

async function logout(){

    await db.auth.signOut();

    location.reload();
}


/* PAGE */

function page(name){

    document.getElementById("people")
        .classList.add("hidden");

    document.getElementById("groups")
        .classList.add("hidden");

    document.getElementById("profile")
        .classList.add("hidden");

    document.getElementById("chat")
        .classList.add("hidden");

    document.getElementById(name)
        .classList.remove("hidden");

    if(name === "people")
        findUsers();

    if(name === "groups")
        loadGroups();

    if(name === "profile")
        loadProfile();
}


/* FIND USERS */

async function findUsers(){

    if(!me) return;

    const q =
        document.getElementById("search")
        .value.trim()
        .toLowerCase();

    let request =
        db
        .from("profiles")
        .select(
            "id,username,display_name,bio"
        )
        .neq("id",me.id)
        .limit(30);

    if(q){

        request =
            request.ilike(
                "username",
                "%" + q + "%"
            );
    }

    const r = await request;

    const box =
        document.getElementById("users");

    box.innerHTML = "";

    if(r.error){

        console.log(r.error);
        return;
    }

    if(!r.data.length){

        box.innerHTML =
            '<div class="empty">No users found</div>';

        return;
    }

    r.data.forEach(function(u){

        const div =
            document.createElement("div");

        div.className = "user";

        const left =
            document.createElement("div");

        const username =
            document.createElement("b");

        username.textContent =
            "@" + u.username;

        const name =
            document.createElement("div");

        name.className = "small";

        name.textContent =
            u.display_name || "";

        left.appendChild(username);
        left.appendChild(name);

        const btn =
            document.createElement("button");

        btn.className = "secondary";
        btn.textContent = "Chat";

        btn.onclick = function(){

            openDirect(
                u.id,
                "@" + u.username
            );
        };

        div.appendChild(left);
        div.appendChild(btn);

        box.appendChild(div);
    });
}


/* OPEN DIRECT CHAT */

async function openDirect(otherId,title){

    const mine =
        await db
        .from("conversation_members")
        .select("conversation_id")
        .eq("user_id",me.id);

    if(!mine.error){

        for(const row of mine.data){

            const c =
                await db
                .from("conversations")
                .select("id")
                .eq("id",row.conversation_id)
                .eq("type","direct")
                .maybeSingle();

            if(!c.data) continue;

            const other =
                await db
                .from("conversation_members")
                .select("user_id")
                .eq(
                    "conversation_id",
                    row.conversation_id
                )
                .eq("user_id",otherId)
                .maybeSingle();

            if(other.data){

                openChat(
                    row.conversation_id,
                    title
                );

                return;
            }
        }
    }


    const created =
        await db
        .from("conversations")
        .insert({
            type:"direct",
            created_by:me.id
        })
        .select()
        .single();

    if(created.error){

        alert(created.error.message);
        return;
    }


    const members =
        await db
        .from("conversation_members")
        .insert([

            {
                conversation_id:created.data.id,
                user_id:me.id
            },

            {
                conversation_id:created.data.id,
                user_id:otherId
            }

        ]);

    if(members.error){

        alert(members.error.message);
        return;
    }

    openChat(
        created.data.id,
        title
    );
}


/* OPEN CHAT */

async function openChat(id,title){

    document.getElementById("people")
        .classList.add("hidden");

    document.getElementById("groups")
        .classList.add("hidden");

    document.getElementById("profile")
        .classList.add("hidden");

    document.getElementById("chat")
        .classList.remove("hidden");

    document.getElementById("chatName")
        .textContent = title;

    currentChat = id;

    await loadMessages();

    subscribe();
}


/* LOAD MESSAGES */

async function loadMessages(){

    const r =
        await db
        .from("messages")
        .select(
            "id,sender_id,content,created_at"
        )
        .eq(
            "conversation_id",
            currentChat
        )
        .order(
            "created_at",
            {ascending:true}
        );

    if(r.error){

        console.log(r.error);
        return;
    }

    const box =
        document.getElementById("messages");

    box.innerHTML = "";

    r.data.forEach(function(m){

        const div =
            document.createElement("div");

        div.className =
            "message" +
            (
                m.sender_id === me.id
                ? " mine"
                : ""
            );

        div.textContent = m.content;

        box.appendChild(div);
    });

    box.scrollTop = box.scrollHeight;
}


/* SEND */

async function send(){

    const input =
        document.getElementById("text");

    const value =
        input.value.trim();

    if(!value || !currentChat)
        return;

    input.value = "";

    const r =
        await db
        .from("messages")
        .insert({
            conversation_id:currentChat,
            sender_id:me.id,
            content:value
        });

    if(r.error){

        alert(r.error.message);
    }
}


/* REALTIME */

function subscribe(){

    if(realtime){

        db.removeChannel(realtime);
    }

    realtime =
        db
        .channel("chat-" + currentChat)
        .on(
            "postgres_changes",
            {
                event:"INSERT",
                schema:"public",
                table:"messages",
                filter:
                "conversation_id=eq." +
                currentChat
            },
            function(){

                loadMessages();
            }
        )
        .subscribe();
}


/* CLOSE */

function closeChat(){

    if(realtime){

        db.removeChannel(realtime);
        realtime = null;
    }

    currentChat = null;

    page("people");
}


/* CREATE GROUP */

async function createGroup(){

    const name =
        document.getElementById("groupName")
        .value.trim();

    if(!name){

        alert("Group name likho.");
        return;
    }

    const r =
        await db
        .from("conversations")
        .insert({
            name:name,
            type:"group",
            created_by:me.id
        })
        .select()
        .single();

    if(r.error){

        alert(r.error.message);
        return;
    }

    const member =
        await db
        .from("conversation_members")
        .insert({
            conversation_id:r.data.id,
            user_id:me.id
        });

    if(member.error){

        alert(member.error.message);
        return;
    }

    document.getElementById("groupName")
        .value = "";

    alert("Group created!");

    loadGroups();
}


/* LOAD GROUPS */

async function loadGroups(){

    const r =
        await db
        .from("conversation_members")
        .select("conversation_id")
        .eq("user_id",me.id);

    const box =
        document.getElementById("groupList");

    box.innerHTML = "";

    if(r.error){

        console.log(r.error);
        return;
    }

    for(const row of r.data){

        const g =
            await db
            .from("conversations")
            .select("id,name")
            .eq("id",row.conversation_id)
            .eq("type","group")
            .maybeSingle();

        if(!g.data) continue;

        const div =
            document.createElement("div");

        div.className = "user";

        const name =
            document.createElement("b");

        name.textContent =
            "👥 " + g.data.name;

        const btn =
            document.createElement("button");

        btn.className = "secondary";
        btn.textContent = "Open";

        btn.onclick = function(){

            openChat(
                g.data.id,
                g.data.name
            );
        };

        div.appendChild(name);
        div.appendChild(btn);

        box.appendChild(div);
    }
}


/* PROFILE */

async function loadProfile(){

    const r =
        await db
        .from("profiles")
        .select("*")
        .eq("id",me.id)
        .single();

    if(r.error){

        console.log(r.error);
        return;
    }

    document.getElementById("profileData")
        .innerHTML =
        "<b>@" +
        safe(r.data.username) +
        "</b>" +
        '<div class="small">' +
        safe(r.data.display_name || "") +
        "</div>";

    document.getElementById("pname")
        .value =
        r.data.display_name || "";

    document.getElementById("pbio")
        .value =
        r.data.bio || "";
}


/* SAVE PROFILE */

async function saveProfile(){

    const name =
        document.getElementById("pname")
        .value.trim();

    const bio =
        document.getElementById("pbio")
        .value.trim();

    const r =
        await db
        .from("profiles")
        .update({
            display_name:name,
            bio:bio
        })
        .eq("id",me.id);

    if(r.error){

        alert(r.error.message);
        return;
    }

    alert("Profile saved!");

    loadProfile();
}


/* SAFE TEXT */

function safe(value){

    const div =
        document.createElement("div");

    div.textContent =
        value == null ? "" : value;

    return div.innerHTML;
}

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE,
        url=SUPABASE_URL,
        key=SUPABASE_KEY
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )from flask import Flask, render_template_string
from supabase import create_client
import os

app = Flask(__name__)

SUPABASE_URL = "https://riolotorwqffbiekspkc.supabase.co"
SUPABASE_KEY = "sb_publishable_nnGkSCQS1X1HnY-1To1zvQ_f5JtX9p"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PAGE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MACAVITY YHE</title>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<style>
body{margin:0;background:#05070a;color:#fff;font-family:Arial}
.app{max-width:650px;min-height:100vh;margin:auto;background:#0c1016}
.header{padding:15px;background:#111a2a;display:flex;justify-content:space-between;border-bottom:1px solid #333}
.box{background:#121c2d;margin:12px;padding:12px;border-radius:12px}
.member{background:#0a1220;padding:10px;margin:6px 0;border-radius:8px;display:flex;justify-content:space-between}
button{padding:6px 14px;border-radius:20px;border:none;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<div class="app">
  <div class="header"><b>MACAVITY-YHE</b><span id="cnt">0 Members</span></div>
  <div class="box">
    <h3>GROUP MEMBERS</h3>
    <div style="display:flex;gap:8px">
      <input id="newM" placeholder="Naya member naam" style="flex:1;padding:10px;border-radius:20px;border:none;background:#1a2538;color:#fff">
      <button onclick="addM()" style="background:#fff;color:#000">+ ADD</button>
    </div>
    <div id="list" style="margin-top:12px">Loading...</div>
  </div>
</div>
<script>
const sb = supabase.createClient("https://riolotorwqffbiekspkc.supabase.co","sb_publishable_nnGkSCQS1X1HnY-1To1zvQ_f5JtX9p")
async function load(){
  let {data} = await sb.from('group_members').select('*').order('id',{ascending:true})
  document.getElementById('cnt').innerText = data.length + " Members"
  document.getElementById('list').innerHTML = data.map(m=> `<div class="member"><span>👤 ${m.username}</span><button onclick="del(${m.id})" style="background:#ff2d2d;color:#fff">Remove</button></div>`).join('')
}
async function addM(){
  let v=document.getElementById('newM').value; if(!v) return alert("naam likh")
  await sb.from('group_members').insert([{username:v}]); document.getElementById('newM').value=""; load()
}
async function del(id){ await sb.from('group_members').delete().eq('id',id); load() }
load()
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
