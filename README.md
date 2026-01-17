# Take-the-Power-Back
# Take the Power Back

A local-first, file-based social system.

No algorithms.  
No centralized feeds.  
No engagement optimization.

Posts, profiles, and connections are represented as files that live with the user.  
This repository documents the core concepts, file specification, and early implementation work.

---

## What This Is

**Take the Power Back** explores a different model of social software:

- Social interaction without a platform-owned network
- Chronological by default
- Manual connections only
- User-owned data stored as files
- No recommendation engines or ranking systems

The system is designed so that *infrastructure is optional* and *ownership is explicit*.

---

## Core Principles

- **Local-first**  
  Data lives on the user’s device or storage provider of choice.

- **File-based**  
  Posts, profiles, and comments are files, not database rows.

- **Chronological**  
  Time ordering is derived from timestamps, not algorithms.

- **Manual social graph**  
  Connections are explicit. No discovery, no suggestions.

- **Client, not platform**  
  This project builds tools that read and write user data.  
  It does not operate a global network.

---

## High-Level Architecture

- Users own a folder that represents their identity
- Social data is stored as structured files (JSON + media)
- Clients read from and write to these folders
- “Following” is subscribing to another user’s folder
- Aggregation happens locally in the client

There is no required backend service.

---

## File-Based Model (Overview)

Each user has a directory containing:

- `profile.json` – identity and metadata
- `posts/` – one file per post
- `comments/` – one file per comment
- `media/` – images and attachments

Files reference each other using IDs.
Ordering is derived from timestamps.
Conflicts are resolved client-side.

Detailed specifications live in `/spec`.

---

## What This Is Not

- Not a social media platform
- Not a feed optimized for engagement
- Not an algorithmic recommendation system
- Not a decentralized blockchain project
- Not designed for virality or scale-by-default

Scale is achieved by *not* creating a global graph.

---

## Current Status

This repository is in **early exploration**.

Initial focus:
- Define a minimal, durable file specification
- Validate the model with a simple client
- Prove that useful social interaction does not require centralized infrastructure

Expect rough edges.

---

## Repository Structure (Early)

---

## Design Constraints (Non-Negotiable)

- No ranking or recommendation algorithms
- No central feed service
- No mandatory accounts or hosted identities
- No dark patterns or engagement metrics

If a feature requires violating these constraints, it does not belong here.

---

## License

TBD.

This will likely be a permissive license to encourage experimentation and forks.
