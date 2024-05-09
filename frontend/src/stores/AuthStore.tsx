import { createStore } from "solid-js/store";

interface UserPublic {
  userid: string;
  username: string;
  displayname: string;
  created: string;
}

const [sessionStore, setSessionStore] = createStore({
  isAuthenticated: false,
  token: "",
  displayname: "",
  username: "",
  userid: "",
});

async function sessionStoreSignIn(token: string) {
  setSessionStore("isAuthenticated", true);
  setSessionStore("token", token);
  sessionStorage.setItem("token", token);
  await updateMeta(token);
}

async function sessionStoreSignOut() {
  setSessionStore("isAuthenticated", false);
  setSessionStore("token", "");
  await updateMeta(null);
}

async function updateMeta(token: string | null) {
  const res = await fetch("/api/v1/users/whoami", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "jwt-token": token ?? "", // TODO: Use Authorization Bearer in the future
    },
  });
  const body: UserPublic = await res.json();
  setSessionStore("displayname", body.displayname);
  setSessionStore("username", body.username);
  setSessionStore("userid", body.userid || "");
}

async function sessionStoreRestore() {
  const token = localStorage.getItem("token") || sessionStorage.token;
  if (token) {
    sessionStoreSignIn(token);
  } else {
    sessionStoreSignOut();
  }
  console.log("Restored sessionStore", sessionStore);
}

await sessionStoreRestore();

export { sessionStore, sessionStoreSignIn, sessionStoreSignOut };
