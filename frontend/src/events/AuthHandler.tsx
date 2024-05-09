import { action } from "@solidjs/router";
import { sessionStore, sessionStoreSignIn } from "../stores/AuthStore";

interface SignInData {
  username: string;
  password: string;
}

async function signIn(data: SignInData): Promise<string> {
  const res = await fetch("/api/v1/users/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: data.username,
      password: data.password,
    }),
  });
  const body: any = await res.json();
  return res.status === 200 ? body.token : "";
}

interface SignUpData {
  email: string;
  username: string;
  password: string;
}

async function signUp(data: SignUpData): Promise<boolean> {
  const res = await fetch("/api/v1/users/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: data.email,
      username: data.username,
      password: data.password,
    }),
  });
  return res.status === 200;
}

const signInHandler = action(async (data) => {
  const token: string = await signIn({
    username: data.get("username"),
    password: data.get("password"),
  });
  if (token === "") {
    return;
  }
  await sessionStoreSignIn(token);
  if (data.get("remember")) {
    localStorage.setItem("token", token);
  }
});

const signUpHandler = action(async (data) => {
  const success: boolean = await signUp({
    email: data.get("email"),
    username: data.get("username"),
    password: data.get("password"),
  });
  if (!success) {
    return;
  }
  const token: string = await signIn({
    username: data.get("username"),
    password: data.get("password"),
  });
  if (token === "") {
    return;
  }
  await sessionStoreSignIn(token);
  if (data.get("remember")) {
    localStorage.setItem("token", token);
  }
});

export { signInHandler, signUpHandler };
