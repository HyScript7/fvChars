import { Component, createSignal, Setter } from "solid-js";

export const AuthForm: Component =  () => {
  const [showSignUp, setShowSignUp] = createSignal<number>(0);

  const handleToggle = () => setShowSignUp((prev) => (prev + 1) % 2);

  return (
    <div class="absolute z-10 bg-base-100 bg-opacity-50">
      <div class="min-h-[100vh] flex flex-col justify-center min-w-[100vw]">
        <div class="mx-auto card w-96 bg-base-200 shadow-xl min-h-[40vh]">
          {showSignUp() === 1 ? (
            <SignUpForm setter={setShowSignUp} toggle={handleToggle} />
          ) : (
            <SignInForm setter={setShowSignUp} toggle={handleToggle} />
          )}
        </div>
      </div>
    </div>
  );
};

interface FormProps {
  setter: Setter<number>;
  toggle: () => void;
}

export const SignInForm: Component<FormProps> = ({ setter, toggle }) => {
  return (
    <div class="card-body">
      <div class="text-center">
        <p class="text-2xl text-cyan-500">Fusionverse Characters</p>
        <p class="text-xl text-cyan-500">Sign In</p>
      </div>
      <hr class="border-cyan-800" />
      <form action="?">
        <div class="flex flex-col gap-2">
          <label class="input input-bordered flex items-center gap-2">
            <input
              type="text"
              class="grow max-w-full"
              placeholder="Username"
              value="username"
            />
          </label>
          <label class="input input-bordered flex items-center gap-2">
            <input
              type="password"
              class="grow max-w-full"
              placeholder="Password"
              value="Password"
            />
          </label>
          <button
            onClick={() => alert("Login button clicked")}
            type="button"
            class="btn bg-cyan-500 text-black hover:bg-cyan-700"
          >
            Login
          </button>
        </div>
      </form>
      <p class="text-sm text-base-500">
        Don't have an account?{" "}
        <button
          type="button"
          onClick={toggle}
          class="link text-cyan-600 hover:text-cyan-700"
        >
          Sign up
        </button>{" "}
        instead!
      </p>
    </div>
  );
};

interface SignUpFormProps {
  setter: Setter<number>;
  toggle: () => void;
}

export const SignUpForm: Component<SignUpFormProps> = ({ setter, toggle }) => {
  return (
    <div class="card-body">
      <div class="text-center">
        <p class="text-2xl text-cyan-500">Fusionverse Characters</p>
        <p class="text-xl text-cyan-500">Sign Up</p>
      </div>
      <hr class="border-cyan-800" />
      <form action="?">
        <div class="flex flex-col gap-2">
          <label class="input input-bordered flex items-center gap-2">
            <input
              type="email"
              class="grow max-w-full"
              placeholder="Email"
              value="example@example.com"
            />
          </label>
          <label class="input input-bordered flex items-center gap-2">
            <input
              type="text"
              class="grow max-w-full"
              placeholder="Username"
              value="username"
            />
          </label>
          <label class="input input-bordered flex items-center gap-2">
            <input
              type="password"
              class="grow max-w-full"
              placeholder="Password"
              value="Password"
            />
          </label>
          <label class="input input-bordered flex items-center gap-2">
            <input
              type="password"
              class="grow max-w-full"
              placeholder="Repeat Password"
              value="Password"
            />
          </label>
          <button
            onClick={() => alert("Register button clicked")}
            type="button"
            class="btn bg-cyan-500 text-black hover:bg-cyan-700"
          >
            Register
          </button>
        </div>
      </form>
      <p class="text-sm text-base-500">
        Already have an account?{" "}
        <button
          type="button"
          onClick={toggle}
          class="link text-cyan-600 hover:text-cyan-700"
        >
          Sign in
        </button>{" "}
        instead!
      </p>
    </div>
  );
};

export default AuthForm;
