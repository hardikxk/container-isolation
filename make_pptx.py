#!/usr/bin/env python3
"""
Generate a PowerPoint presentation for:
Container Isolation: Docker Containers & Cloud Computing
"""

import os

from pptx import Presentation
from pptx.util import Inches, Pt

OUTPUT_FILENAME = "Container_Isolation.pptx"

# Create presentation in 16:9
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

IMG_DIR = "images"

def add_image_slide(title, filename, notes=""):
    """Slide with a big centred diagram (falls back to a warning box)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.25), Inches(12.5), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True

    path = os.path.join(IMG_DIR, filename)
    if os.path.exists(path):
        slide.shapes.add_picture(path, Inches(1.17), Inches(1.35), width=Inches(11.0))
    else:
        warn = slide.shapes.add_textbox(Inches(2.5), Inches(3.2), Inches(8.3), Inches(1.4))
        wp = warn.text_frame.paragraphs[0]
        wp.text = f"[Image missing: {path}]\nRun:  python generate_diagrams.py"
        wp.font.size = Pt(20)

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

def add_title_slide(title, subtitle, notes=""):
    """Add a title slide."""
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = title

    if len(slide.placeholders) > 1:
        slide.placeholders[1].text = subtitle

    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def add_bullet_slide(title, bullets, notes=""):
    """
    Add a bullet-point slide.
    bullets can be:
      - "text" for level 0
      - ("text", level) for indentation
    """
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = title

    body_shape = slide.placeholders[1]
    text_frame = body_shape.text_frame
    text_frame.clear()

    for i, item in enumerate(bullets):
        if isinstance(item, tuple):
            text, level = item
        else:
            text, level = item, 0

        if i == 0:
            paragraph = text_frame.paragraphs[0]
        else:
            paragraph = text_frame.add_paragraph()

        paragraph.text = text
        paragraph.level = level

        if level == 0:
            paragraph.font.size = Pt(24)
        else:
            paragraph.font.size = Pt(20)

        paragraph.space_after = Pt(8)

    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def add_code_slide(title, code, notes=""):
    """Add a slide with a title and monospaced code/text diagram."""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Title box
    title_left = Inches(0.4)
    title_top = Inches(0.25)
    title_width = Inches(12.5)
    title_height = Inches(0.9)

    title_box = slide.shapes.add_textbox(
        title_left, title_top, title_width, title_height
    )
    title_frame = title_box.text_frame
    title_frame.word_wrap = True

    title_paragraph = title_frame.paragraphs[0]
    title_paragraph.text = title
    title_paragraph.font.size = Pt(32)
    title_paragraph.font.bold = True

    # Code box
    code_left = Inches(0.4)
    code_top = Inches(1.25)
    code_width = Inches(12.5)
    code_height = Inches(5.7)

    code_box = slide.shapes.add_textbox(
        code_left, code_top, code_width, code_height
    )
    code_frame = code_box.text_frame
    code_frame.word_wrap = True

    lines = code.splitlines()

    for i, line in enumerate(lines):
        if i == 0:
            paragraph = code_frame.paragraphs[0]
        else:
            paragraph = code_frame.add_paragraph()

        paragraph.text = line if line.strip() else " "
        paragraph.font.name = "Consolas"
        paragraph.font.size = Pt(14)
        paragraph.space_after = Pt(2)

    if notes:
        slide.notes_slide.notes_text_frame.text = notes


# ------------------------------------------------------------
# Slide 1: Title
# ------------------------------------------------------------
add_title_slide(
    title="Container Isolation: How Docker Tricks the OS",
    subtitle=(
        "Case Study: Docker Containers & Cloud Computing\n"
        "Operating Systems Class Presentation"
    ),
    notes=(
        "Good morning/afternoon. Today I will explain container isolation "
        "using Docker as a case study. The main idea is that containers "
        "are not full virtual machines. They are ordinary Linux processes "
        "wrapped with kernel isolation features."
    )
)

# ------------------------------------------------------------
# Slide 2: Agenda
# ------------------------------------------------------------
add_bullet_slide(
    title="Agenda",
    bullets=[
        "Introduction to containers",
        "Virtual machines vs containers",
        "Linux namespaces",
        "Control groups (cgroups)",
        "Overlay filesystems",
        "Security layers",
        "Docker execution model",
        "Containers in cloud computing",
        "Limitations and security concerns",
        "Conclusion",
    ],
    notes=(
        "We will first compare containers with virtual machines, then "
        "discuss the four main isolation mechanisms: namespaces, cgroups, "
        "overlay filesystems, and security layers. Finally, we will look "
        "at cloud computing use and limitations."
    )
)

# ------------------------------------------------------------
# Slide 3: What Is a Container?
# ------------------------------------------------------------
add_bullet_slide(
    title="What Is a Container?",
    bullets=[
        "A lightweight, isolated user-space environment",
        "Shares the host operating system kernel",
        "Packages application code, libraries, and dependencies",
        "Faster and lighter than a full virtual machine",
        "Uses Linux kernel features such as namespaces and cgroups",
    ],
    notes=(
        "A container looks like a separate machine to the application inside it, "
        "but from the kernel's point of view it is just a process with restricted "
        "visibility and limited resources."
    )
)
# after the "What Is a Container?" bullet slide
add_image_slide("Virtual Machines vs Containers", "vm_vs_container.png",
    "VMs duplicate the whole OS per workload; containers share one kernel.")


# ------------------------------------------------------------
# Slide 4: VM vs Container
# ------------------------------------------------------------
add_bullet_slide(
    title="Virtual Machines vs Containers",
    bullets=[
        ("Virtual machines emulate complete hardware", 0),
        ("Require a hypervisor such as VMware, KVM, or VirtualBox", 1),
        ("Each VM runs a full guest operating system", 1),
        ("Containers use OS-level isolation", 0),
        ("Containers share the host kernel", 1),
        ("Containers start in milliseconds to seconds", 1),
        ("VMs provide stronger isolation but higher overhead", 0),
        ("Containers provide faster deployment and higher density", 0),
    ],
    notes=(
        "Virtual machines emulate complete hardware and run separate operating systems. "
        "Containers share the host kernel, so they are faster and lighter, but their "
        "isolation boundary is not as strong as a full VM."
    )
)

# ------------------------------------------------------------
# Slide 5: Namespaces
# ------------------------------------------------------------
add_bullet_slide(
    title="Pillar 1: Linux Namespaces",
    bullets=[
        "Namespaces control what a process can see",
        "PID namespace: isolates process IDs",
        "NET namespace: isolates network interfaces and ports",
        "MNT namespace: isolates mount points",
        "UTS namespace: isolates hostname",
        "IPC namespace: isolates inter-process communication",
        "USER namespace: isolates user and group IDs",
        "Each container gets a private view of the system",
    ],
    notes=(
        "Namespaces provide visibility isolation. For example, a process inside "
        "a container can believe it is PID 1, even though on the host it has "
        "a completely different PID."
    )
)

# ------------------------------------------------------------
# Slide 6: Cgroups
# ------------------------------------------------------------
add_bullet_slide(
    title="Pillar 2: Control Groups (cgroups)",
    bullets=[
        "Cgroups control how much resource a container can use",
        "CPU: limit percentage of processor time",
        "Memory: set hard memory limits",
        "Block I/O: limit disk read/write bandwidth",
        "PIDs: limit number of processes",
        "Devices: allow or deny device access",
        "Prevents one container from starving others",
    ],
    notes=(
        "If namespaces control visibility, cgroups control quantity. "
        "They are important in cloud environments because many containers "
        "share the same physical machine."
    )
)

# after the namespaces / cgroups bullet slides
add_image_slide("Namespaces vs Cgroups: See vs Use", "namespaces_cgroups.png",
    "Namespaces control visibility; cgroups control quantity.")

# ------------------------------------------------------------
# Slide 7: Overlay Filesystem
# ------------------------------------------------------------
overlay_code = """
Container Writable Layer
-----------------------------------
Read-only Layer 3: Application code
Read-only Layer 2: Libraries/runtime
Read-only Layer 1: Base OS image
"""

add_code_slide(
    title="Pillar 3: Overlay Filesystems",
    code=overlay_code.strip(),
    notes=(
        "Overlay filesystems give each container a private filesystem view. "
        "The container can modify files, but changes are stored in its own "
        "writable layer and do not affect other containers."
    )
)

# after the overlay filesystem slide
add_image_slide("Overlay Filesystem Layers", "overlayfs.png",
    "Only the writable layer differs per container; base layers are shared.")


# ------------------------------------------------------------
# Slide 8: Security Layers
# ------------------------------------------------------------
add_bullet_slide(
    title="Pillar 4: Security Layers",
    bullets=[
        "Cgroups limit resource usage",
        "Namespaces isolate visibility",
        "Linux capabilities remove unnecessary root privileges",
        "Seccomp-BPF restricts allowed system calls",
        "AppArmor or SELinux enforces mandatory access control",
        "Docker uses defense-in-depth",
    ],
    notes=(
        "Container isolation is not based on one magic feature. "
        "It combines several kernel mechanisms to reduce the attack surface."
    )
)


# after the security layers slide
add_image_slide("Defence in Depth", "security_layers.png",
    "An attacker must bypass every ring, not just one mechanism.")


# ------------------------------------------------------------
# Slide 9: Docker Execution Model
# ------------------------------------------------------------
docker_flow_code = """
docker CLI -> dockerd -> containerd -> runc

runc performs:
  1. clone() with namespace flags
  2. cgroup resource setup
  3. filesystem setup with pivot_root()
  4. capability dropping and seccomp filtering
  5. exec() of container entrypoint
"""

add_code_slide(
    title="How Docker Launches a Container",
    code=docker_flow_code.strip(),
    notes=(
        "When a user runs docker run, the Docker daemon eventually asks runc "
        "to create the container. runc is the low-level component that interacts "
        "directly with Linux kernel isolation features."
    )
)


# after the Docker execution model slide
add_image_slide("Inside docker run", "docker_architecture.png",
    "CLI -> dockerd -> containerd -> runc -> kernel primitives.")

# ------------------------------------------------------------
# Slide 10: Example Docker Command
# ------------------------------------------------------------
docker_command_code = """
docker run -d --name web \\
  --memory=256m \\
  --cpus=0.5 \\
  --read-only \\
  --tmpfs /tmp \\
  --security-opt=no-new-privileges \\
  nginx:alpine
"""

add_code_slide(
    title="Example Docker Command",
    code=docker_command_code.strip(),
    notes=(
        "This single command creates namespaces, cgroups, filesystem isolation, "
        "and security restrictions for the container."
    )
)

# ------------------------------------------------------------
# Slide 11: Live Demo Ideas
# ------------------------------------------------------------
demo_code = """
docker run -d --name demo --memory=128m --cpus=0.5 nginx:alpine

docker top demo

ps aux | grep nginx

docker inspect demo --format '{{.HostConfig.Memory}}'

PID=$(docker inspect -f '{{.State.Pid}}' demo)

ls -l /proc/$PID/ns/
"""

add_code_slide(
    title="Class Demo: Observing Isolation",
    code=demo_code.strip(),
    notes=(
        "This demo shows that the container process has one PID inside the "
        "container but another PID on the host. The /proc namespace listing "
        "shows the separate namespaces assigned to the container."
    )
)

# ------------------------------------------------------------
# Slide 12: Containers in Cloud Computing
# ------------------------------------------------------------
add_bullet_slide(
    title="Containers in Cloud Computing",
    bullets=[
        "Cloud providers use containers for fast scaling",
        "Many workloads can share the same physical server",
        "Kubernetes manages containers across many machines",
        "Managed services include AWS EKS, Google GKE, Azure AKS",
        "Serverless platforms often use containers or microVMs",
        "Isolation enables multi-tenant cloud environments",
    ],
    notes=(
        "Cloud computing depends heavily on isolation. Containers allow providers "
        "to run many workloads on the same physical servers while maintaining "
        "separation between applications."
    )
)


# after the cloud computing slide
add_image_slide("Kubernetes: Isolation at Cloud Scale", "kubernetes_cluster.png",
    "Control plane schedules pods; policies extend isolation cluster-wide.")


# ------------------------------------------------------------
# Slide 13: Isolation Strength Spectrum
# ------------------------------------------------------------
spectrum_code = """
Weaker Isolation <---------------------------------------> Stronger Isolation

chroot        Docker        gVisor/user-space kernel        Kata/Firecracker        Full VM
"""

add_code_slide(
    title="Isolation Strength Spectrum",
    code=spectrum_code.strip(),
    notes=(
        "Containers are not the strongest possible isolation mechanism. "
        "For untrusted code, cloud providers may add gVisor, Kata Containers, "
        "Firecracker microVMs, or full virtual machines."
    )
)


# before the limitations slide
add_image_slide("Isolation Strength Spectrum", "isolation_spectrum.png",
    "Isolation is a dial: containers are mid-spectrum; microVMs and VMs are stronger.")



# ------------------------------------------------------------
# Slide 14: Limitations
# ------------------------------------------------------------
add_bullet_slide(
    title="Limitations and Security Concerns",
    bullets=[
        "Containers share the host kernel",
        "A kernel vulnerability may affect all containers",
        "Privileged containers weaken isolation",
        "Side-channel attacks may cross container boundaries",
        "Malicious images can introduce vulnerabilities",
        "Network traffic may need encryption",
    ],
    notes=(
        "Containers provide strong practical isolation, but they are not as hard "
        "a boundary as full virtual machines. For untrusted code, stronger "
        "isolation technologies should be used."
    )
)

# ------------------------------------------------------------
# Slide 15: Key Takeaways
# ------------------------------------------------------------
add_bullet_slide(
    title="Key Takeaways",
    bullets=[
        "Containers are isolated processes, not full virtual machines",
        "Namespaces control what a container can see",
        "Cgroups control how much resource a container can use",
        "Overlay filesystems provide private filesystem views",
        "Security layers reduce privileges and system-call access",
        "Containers are central to modern cloud computing",
    ],
    notes=(
        "To summarize, container isolation is built from several operating system "
        "mechanisms working together. This is why containers are lightweight, "
        "fast, and useful for cloud deployment, but still require careful security."
    )
)

# ------------------------------------------------------------
# Slide 16: Q&A
# ------------------------------------------------------------
add_bullet_slide(
    title="Questions?",
    bullets=[
        "Thank you for listening",
        "Any questions?",
    ],
    notes=(
        "Thank the audience and invite questions."
    )
)

# Save the presentation
prs.save(OUTPUT_FILENAME)

print(f"Created {OUTPUT_FILENAME}")
