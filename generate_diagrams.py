#!/usr/bin/env python3
"""Generate licence-free diagrams for the Container Isolation presentation."""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

OUT = "images"
os.makedirs(OUT, exist_ok=True)

NAVY, BLUE, LBLUE = "#1B4F72", "#2E86C1", "#AED6F1"
GREEN, LGREEN     = "#1E8449", "#A9DFBF"
ORANGE            = "#E67E22"
PURPLE            = "#7D3C98"
RED               = "#C0392B"
GRAY, LGRAY       = "#7F8C8D", "#E5E8E8"
WHITE, INK        = "#FFFFFF", "#212F3D"

def new_fig(w=13, h=6.75):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax

def box(ax, x, y, w, h, text, fc=BLUE, ec="white", tc="white", fs=11, bold=True):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=1.6, zorder=2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", color=tc,
            fontsize=fs, fontweight=("bold" if bold else "normal"), zorder=3)

def label(ax, x, y, text, fs=12, color=INK, ha="center", bold=True):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fs, color=color,
            fontweight=("bold" if bold else "normal"))

def arrow(ax, x1, y1, x2, y2, color="#444444", lw=2.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=18, lw=lw, color=color, zorder=4))

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved:", path)

# ---------------- 1. VM vs Container ----------------
def vm_vs_container():
    fig, ax = new_fig()
    label(ax, 25, 96, "VIRTUAL MACHINES", fs=15, color=RED)
    label(ax, 75, 96, "CONTAINERS", fs=15, color=GREEN)
    for i, x in enumerate([5, 19, 33]):
        box(ax, x, 78, 12, 9, f"App {chr(65+i)}", fc=BLUE)
        box(ax, x, 67, 12, 9, "Bins / Libs", fc=LBLUE, tc=INK)
        box(ax, x, 56, 12, 9, "Guest OS", fc=PURPLE)
    box(ax, 5, 43, 40, 10, "HYPERVISOR  (VMware / KVM / Hyper-V)", fc=RED)
    box(ax, 5, 31, 40, 10, "Host Operating System", fc=NAVY)
    box(ax, 5, 19, 40, 10, "HARDWARE", fc=GRAY)
    label(ax, 25, 10, "Heavy: GB images, minutes to boot,\nfull guest OS per workload", fs=11, color=RED)
    for i, x in enumerate([55, 69, 83]):
        box(ax, x, 78, 12, 9, f"App {chr(65+i)}", fc=BLUE)
        box(ax, x, 67, 12, 9, "Bins / Libs", fc=LBLUE, tc=INK)
    box(ax, 55, 54, 40, 10, "CONTAINER ENGINE  (Docker / containerd)", fc=GREEN)
    box(ax, 55, 42, 40, 10, "Host Operating System  (shared Linux kernel)", fc=NAVY)
    box(ax, 55, 30, 40, 10, "HARDWARE", fc=GRAY)
    label(ax, 75, 10, "Light: MB images, millisecond start,\nkernel shared by all containers", fs=11, color=GREEN)
    ax.plot([50, 50], [15, 92], color="#BBBBBB", lw=1.5, ls="--")
    save(fig, "vm_vs_container.png")

# ---------------- 2. Namespaces + cgroups ----------------
def namespaces_cgroups():
    fig, ax = new_fig()
    ax.add_patch(Rectangle((4, 40), 92, 52, facecolor="#EAF2F8", edgecolor=NAVY, lw=2))
    label(ax, 50, 88, "HOST  —  what each process can SEE  (namespaces)", fs=13, color=NAVY)
    for i, x in enumerate([8, 37, 66]):
        box(ax, x, 58, 26, 24,
            f"CONTAINER {i+1}\n\nPID ns: own process tree\nNET ns: own eth0 & ports\nMNT ns: own filesystem\nUTS ns: own hostname",
            fc=BLUE, fs=10)
    ax.add_patch(Rectangle((4, 8), 92, 28, facecolor="#FDEDEC", edgecolor=RED, lw=2))
    label(ax, 50, 33, "KERNEL  —  how much each process can USE  (cgroups)", fs=13, color=RED)
    for i, x in enumerate([8, 37, 66]):
        box(ax, x, 12, 26, 16, f"CGROUP {i+1}\nCPU 50% | MEM 256 MB\nI/O 100 MB/s | PIDs 100", fc=RED, fs=10)
        arrow(ax, x + 13, 58, x + 13, 29, color=NAVY)
    save(fig, "namespaces_cgroups.png")

# ---------------- 3. Overlay filesystem ----------------
def overlayfs():
    fig, ax = new_fig(12, 6.75)
    label(ax, 40, 95, "CONTAINER FILESYSTEM VIEW", fs=14)
    box(ax, 15, 74, 50, 13, "WRITABLE LAYER  (container changes, Copy-on-Write)", fc=ORANGE, fs=11)
    box(ax, 15, 59, 50, 13, "read-only layer 3 — application code", fs=11)
    box(ax, 15, 44, 50, 13, "read-only layer 2 — libraries & runtime", fs=11)
    box(ax, 15, 29, 50, 13, "read-only layer 1 — base OS (Alpine/Ubuntu)", fc=LBLUE, tc=INK, fs=11)
    ax.add_patch(Rectangle((11, 29), 2, 43, facecolor=NAVY, edgecolor="none"))
    label(ax, 9.5, 50, "IMAGE", fs=11, color=NAVY, ha="right")
    arrow(ax, 80, 80.5, 66, 80.5, color=ORANGE)
    label(ax, 82, 80.5, "edits land here only", fs=11, color=ORANGE, ha="left")
    label(ax, 40, 18, "100 containers from one image share the same\nread-only layers on disk → huge space savings", fs=12, bold=False)
    label(ax, 40, 8, "deleting a file = 'whiteout' marker hides the lower layer", fs=10, color=GRAY, bold=False)
    save(fig, "overlayfs.png")

# ---------------- 4. Defence in depth ----------------
def security_layers():
    fig, ax = new_fig(12, 6.75)
    rings = [
        (3, 5, 94, 90, "#FDEBD0", "AppArmor / SELinux — mandatory access control"),
        (10, 13, 80, 74, "#FAD7A0", "Seccomp-BPF — system-call filter (~300 syscalls allowed)"),
        (17, 21, 66, 58, "#F8C471", "Linux Capabilities — root powers dropped"),
        (24, 29, 52, 42, "#F5B041", "Namespaces — visibility walls"),
        (31, 37, 38, 26, "#EB984E", "Cgroups — resource limits"),
    ]
    for x, y, w, h, fc, txt in rings:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor="white", lw=2))
        label(ax, x + 1.5, y + h - 3.5, txt, fs=10.5, ha="left")
    box(ax, 38, 44, 24, 12, "container\nprocess", fc=NAVY, fs=11)
    label(ax, 50, 98, "DEFENCE IN DEPTH", fs=15)
    save(fig, "security_layers.png")

# ---------------- 5. Docker architecture ----------------
def docker_architecture():
    fig, ax = new_fig()
    label(ax, 50, 95, "WHAT HAPPENS WHEN YOU TYPE:  docker run", fs=14)
    for name, x, c in [("docker CLI", 4, BLUE), ("dockerd", 28, BLUE),
                       ("containerd", 52, BLUE), ("runc", 76, GREEN)]:
        box(ax, x, 70, 20, 12, name, fc=c, fs=12)
    for x1 in (24, 48, 72):
        arrow(ax, x1, 76, x1 + 4, 76)
    label(ax, 26, 85, "REST API", fs=9, color=GRAY)
    label(ax, 50, 85, "gRPC", fs=9, color=GRAY)
    label(ax, 74, 85, "OCI spec", fs=9, color=GRAY)
    arrow(ax, 86, 70, 86, 57)
    box(ax, 58, 44, 38, 12, "Linux kernel primitives", fc=NAVY, fs=12)
    for txt, x in [("clone() +\nnamespaces", 58), ("cgroup\nlimits", 71), ("pivot_root +\nOverlayFS", 84)]:
        box(ax, x, 24, 12, 14, txt, fc=LBLUE, tc=INK, fs=9)
        arrow(ax, x + 6, 44, x + 6, 39, lw=1.5)
    box(ax, 4, 44, 40, 12, "security hardening:\ndrop capabilities, seccomp, AppArmor", fc=ORANGE, fs=10)
    arrow(ax, 38, 70, 24, 57, lw=1.5)
    label(ax, 50, 10, "runc creates the namespaces, sets cgroups, pivots root and execs the app",
          fs=10.5, color=GRAY, bold=False)
    save(fig, "docker_architecture.png")

# ---------------- 6. Isolation spectrum ----------------
def isolation_spectrum():
    fig, ax = new_fig(13, 5.5)
    arrow(ax, 6, 50, 94, 50, lw=3, color=NAVY)
    pts = [(12, "chroot", "very weak", "#27AE60"),
           (30, "Docker container", "namespaces + cgroups\n+ seccomp", "#2ECC71"),
           (50, "gVisor", "user-space\nkernel", "#F1C40F"),
           (70, "Kata / Firecracker", "microVM", ORANGE),
           (88, "Full VM", "separate kernel", RED)]
    for x, name, desc, c in pts:
        ax.add_patch(Circle((x, 50), 2.2, color=c, zorder=5))
        ax.plot([x, x], [42, 47.5], color=c, lw=1.5)
        ax.plot([x, x], [52.5, 58], color=c, lw=1.5)
        label(ax, x, 63, name, fs=12)
        label(ax, x, 33, desc, fs=9.5, color=GRAY, bold=False)
    label(ax, 8, 82, "LOWER OVERHEAD • FASTER START", fs=11, color=GREEN, ha="left")
    label(ax, 92, 82, "STRONGER ISOLATION", fs=11, color=RED, ha="right")
    label(ax, 50, 12, "Isolation is a dial, not a switch — cloud providers pick per workload",
          fs=11, bold=False)
    save(fig, "isolation_spectrum.png")

# ---------------- 7. Kubernetes cluster ----------------
def kubernetes_cluster():
    fig, ax = new_fig()
    ax.add_patch(Rectangle((3, 4), 94, 92, facecolor="#F8F9F9", edgecolor=NAVY, lw=2))
    label(ax, 50, 92, "KUBERNETES CLUSTER  (AWS EKS / GKE / Azure AKS)", fs=13, color=NAVY)
    box(ax, 30, 78, 40, 10, "Control Plane — API server, scheduler, etcd", fc=PURPLE, fs=10.5)
    for i, x in enumerate([7, 37, 67]):
        ax.add_patch(Rectangle((x, 18), 26, 48, facecolor="white", edgecolor=GREEN, lw=2))
        box(ax, x, 58, 26, 8, f"NODE {i+1}", fc=GREEN, fs=11)
        box(ax, x + 3, 46, 20, 9, "Pod (containers)", fs=9.5)
        box(ax, x + 3, 34, 20, 9, "Pod (containers)", fs=9.5)
        box(ax, x + 3, 22, 20, 8, "kubelet + runtime", fc=LGRAY, tc=INK, fs=9)
        arrow(ax, 50, 78, x + 13, 67, color=PURPLE, lw=1.5)
    label(ax, 50, 10, "NetworkPolicies + ResourceQuotas + Pod Security Standards extend isolation cluster-wide",
          fs=10.5, bold=False)
    save(fig, "kubernetes_cluster.png")

if __name__ == "__main__":
    vm_vs_container()
    namespaces_cgroups()
    overlayfs()
    security_layers()
    docker_architecture()
    isolation_spectrum()
    kubernetes_cluster()
    print("\nAll diagrams generated in ./images/")
