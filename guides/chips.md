# CPU · GPU · TPU · NPU — the chips behind every AI

> @geekylax_ai · 100 Days of GenAI

Every AI model you touch runs on silicon — but not all silicon is equal. A chatbot reply, a photo-unlock on your phone, and the training run behind a frontier model each live on a *different* kind of processor. Here's the clean mental model: four chip families, what each is actually good at, and why the whole world suddenly can't get enough of them.

**The one-line map:**

| Chip | Built for | Sweet spot | Lives in |
|------|-----------|-----------|----------|
| **CPU** | A few complex tasks, fast and in order | Logic, control, orchestration | Every computer |
| **GPU** | Thousands of simple math ops in parallel | AI **training** + heavy inference | Data centers, gaming PCs |
| **TPU** | Matrix math, nothing else | Large-scale training + inference | Google data centers |
| **NPU** | Low-power neural inference | **On-device / edge** AI | Phones, laptops |

The through-line: AI is mostly **matrix multiplication** done billions of times. The more a chip specializes in that one operation — and strips away everything else — the faster and more efficient it gets. That trade-off is the whole story.

---

## CPU — the generalist

**What it is.** The Central Processing Unit is the brain that runs *everything else*: your operating system, your browser, the Python script that calls the AI model. It has a handful of very powerful cores (typically 4–64) built to execute a complex sequence of instructions as fast as possible, one dependency after another.

**How it differs.** A CPU optimizes for **latency on serial work** — finish this hard, branchy task *now*. It carries big caches, sophisticated branch prediction, and out-of-order execution. What it does *not* have is thousands of parallel math units, so it chokes on the dense, repetitive arithmetic that neural networks demand.

**Best for AI.** Orchestration, data loading and preprocessing, running the glue code, and small or latency-sensitive models where spinning up a GPU isn't worth it. In almost every AI system the CPU is the conductor, not the muscle.

**Real examples.** Intel Core / Xeon, AMD Ryzen / EPYC, Apple M-series (its CPU cores), and the Arm cores in virtually every phone.

**Learn it**
- 🎥 [Inside the CPU — Computerphile](https://www.youtube.com/watch?v=IAkj32VPcUE) — a clear, short walk through what a CPU core actually does each cycle.

---

## GPU — the parallel workhorse of AI

**What it is.** The Graphics Processing Unit was built to shade millions of pixels at once, which means **thousands of small cores doing the same math in parallel**. That architecture turned out to be a near-perfect match for neural networks, which are oceans of parallel multiply-add operations. Modern AI GPUs add dedicated **Tensor Cores** that chew through matrix math at low precision (FP16, FP8, even FP4).

**How it differs.** Where a CPU optimizes latency, a GPU optimizes **throughput** — do a staggering *amount* of math per second, even if any single operation isn't rushed. The software moat is just as important: **CUDA**, Nvidia's programming platform, is why most AI frameworks (PyTorch, TensorFlow) target Nvidia hardware by default.

**Best for AI.** The default chip for **training** large models, and the workhorse for high-volume **inference** in data centers. Flexible enough to run anything, fast enough to matter — which is exactly why it dominates.

**Real examples.** Nvidia **H100** (Hopper) and the newer **Blackwell** generation (GB200 / B200) power most frontier AI data centers; AMD Instinct (MI300) is the main challenger; consumer RTX cards run AI locally.

**Learn it**
- 📘 [NVIDIA CUDA](https://developer.nvidia.com/cuda-zone) — the platform that made GPUs the home of AI compute.
- 📘 [NVIDIA H100 Tensor Core GPU](https://www.nvidia.com/en-us/data-center/h100/) — the Hopper-architecture workhorse behind this AI era.
- 📘 [NVIDIA Blackwell architecture](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/) — the current generation, with FP4 and a second-gen Transformer Engine.
- 📄 [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — the Transformer paper; this architecture is what made GPU-scale matrix math indispensable.

---

## TPU — Google's purpose-built AI chip

**What it is.** The Tensor Processing Unit is an **ASIC** (application-specific chip) Google designed to do essentially one thing: the matrix multiplications at the heart of neural networks. It uses a **systolic array** — a grid of multiply-add units that passes data through in a rhythmic wave — so it skips much of the general-purpose overhead a GPU still carries.

**How it differs.** A GPU is a flexible parallel processor; a TPU throws away flexibility to win on **matrix-math efficiency per watt**. It pairs tightly with Google's software stack (JAX, TensorFlow, XLA) and scales into large "pods" wired together for huge training jobs.

**Best for AI.** Large-scale **training and inference** inside Google's infrastructure — the kind of workload where you control the whole stack and want maximum performance-per-dollar at scale. Less about flexibility, more about doing one thing extremely well.

**Real examples.** Google **TPU** v2 → v5 → Trillium / Ironwood generations, available to anyone through **Google Cloud**; they train and serve Google's own Gemini models.

**Learn it**
- 📄 [In-Datacenter Performance Analysis of a Tensor Processing Unit (Jouppi et al., 2017)](https://arxiv.org/abs/1704.04760) — the landmark paper measuring the first TPU against CPUs and GPUs.
- 🔗 [An in-depth look at Google's first TPU](https://cloud.google.com/blog/products/ai-machine-learning/an-in-depth-look-at-googles-first-tensor-processing-unit-tpu) — Google's own plain-English explainer of the systolic array idea.
- 📘 [Cloud TPU](https://cloud.google.com/tpu) — the current TPU generations and how to use them.

---

## NPU — AI that runs in your pocket

**What it is.** The Neural Processing Unit (a.k.a. AI accelerator or neural engine) is a small, hyper-efficient block built into phone and laptop chips to run neural networks **on the device, at very low power**. It trades raw peak throughput for **performance-per-milliwatt** — so Face ID, live translation, computational photography, and on-device assistants can run without draining the battery or sending your data to a server.

**How it differs.** A data-center GPU/TPU maximizes absolute speed and can burn hundreds of watts. An NPU maximizes **efficiency and privacy** inside a power budget of a few watts, almost always for **inference only** — not training.

**Best for AI.** **Edge / on-device inference**: real-time, private, always-available AI where round-tripping to the cloud is too slow, too costly, or too sensitive.

**Real examples.** Apple **Neural Engine** (in iPhone / Mac A- and M-series chips), Qualcomm Hexagon NPU (Snapdragon), Google Tensor, and the NPUs in Intel / AMD "AI PC" laptops powering Copilot+ features.

**Learn it**
- 📘 [Apple Core ML](https://developer.apple.com/documentation/coreml) — Apple's framework for running models on-device across CPU, GPU, and the Neural Engine.
- 📄 [Deploying Transformers on the Apple Neural Engine](https://machinelearning.apple.com/research/neural-engine-transformers) — Apple's own guide, showing why on-device inference means your data never leaves the device.

---

## Why the AI chip boom matters

AI's appetite for compute collided with the fact that these chips are among the **hardest objects humanity knows how to make** — and that scarcity reshaped the tech economy.

**GPUs + CUDA = the moat.** When deep learning took off, Nvidia already had the parallel hardware *and* **CUDA**, a mature software ecosystem every AI researcher was trained on. That combination made Nvidia the default supplier of AI compute and, for a stretch, one of the most valuable companies on Earth. Every frontier lab's capability is gated by how many GPUs it can get.

**The supply chain is a single thread.** Nvidia (and Google, Apple, AMD) **design** chips but don't manufacture them. Almost all leading-edge AI silicon is fabricated by one company: **TSMC** in Taiwan. The whole industry's most advanced chips funnel through a handful of its fabs — a concentration with no real backup.

**And TSMC depends on one machine.** To print transistors only nanometers apart, modern chips need **EUV (extreme ultraviolet) lithography** — light at a 13.5 nm wavelength, generated by blasting molten tin droplets with a laser ~50,000 times a second, focused entirely by mirrors in a vacuum because EUV is absorbed by air and even glass. Exactly **one company on the planet**, **ASML** in the Netherlands, builds these machines. Each costs hundreds of millions of dollars.

**The takeaway:** the AI boom rests on a startlingly narrow pyramid — Nvidia's designs, made by TSMC, using ASML's EUV machines. Understand that chain and you understand why AI chips are a geopolitical story, not just a tech one.

**Learn it**
- 🎥 [The Closest Thing We Have to Alien Technology — Veritasium](https://www.youtube.com/watch?v=MiUHjLxm3V0) — a deep, visual tour of ASML's EUV machine and why it's irreplaceable.
- 📘 [ASML — EUV lithography systems](https://www.asml.com/en/products/euv-lithography-systems) — the maker's own page on the machines that print every advanced chip.
- 📘 [ASML — Light & lasers](https://www.asml.com/en/technology/lithography-principles/light-and-lasers) — how the tin-droplet EUV light source actually works.
- 📘 [TSMC — Logic technology](https://www.tsmc.com/english/dedicatedFoundry/technology/logic) — the advanced process nodes (2nm and below) where the world's AI chips are made.

---

### The 10-second recap

- **CPU** = the conductor: a few fast cores running everything in order.
- **GPU** = the workhorse: thousands of cores for parallel math — AI's default for training.
- **TPU** = the specialist: an ASIC built only for matrix math, at Google scale.
- **NPU** = the pocket chip: low-power neural inference, on-device and private.
- **The boom** = Nvidia + CUDA on top, made by TSMC, using ASML's EUV machines — a very narrow, very critical pyramid.
