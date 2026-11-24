"""Üç özgün palet. Rol adları tüm yönlerde ortak -> sahne şablonları paletten bağımsız."""
A = dict(  # Yön A — "Mürekkep & Kiremit"
  name="A · Mürekkep & Kiremit", paper="#F7F1E5", ink="#1D1A17",
  accent="#E4572E", accent2="#2A7F7A", hide="#C8955A", hair="#3B2A20", shade="#E7DFD0", blush="#F29E8A",
  cap="#5B6E8C", nose="#E9967A", hair2="#3B2A20",
  sky="#CFE2E3", sky2="#EEF3EC", hill="#A9BFA0", ground="#D9B27C", ground2="#B98A55", stone="#B9AFA2", stone2="#8E8478",
  night="#17233A", night2="#2C3B57", fire="#F28C28", fire2="#FFD166",
  wall="#F2DCC2", floor="#C99A6B", sofa="#2A7F7A", red="#B83A2B", green="#3E9C5B")  # red: C yönünden (5,2:1)
B = dict(  # Yön B — "Kobalt Defter"
  name="B · Kobalt Defter", paper="#F4F3EE", ink="#1D1A17",
  accent="#3556C9", accent2="#FF6B57", hide="#B7864F", hair="#2B2D33", shade="#E3E3DC", blush="#F7A08E",
  cap="#6F7D5C", nose="#E8907E", hair2="#2B2D33",
  sky="#D6E4EF", sky2="#F1F5F7", hill="#B9C7B4", ground="#E6D2A0", ground2="#C7AC74", stone="#C5C2BA", stone2="#97948C",
  night="#151B34", night2="#28325A", fire="#FF8A3D", fire2="#FFD45C",
  wall="#E9EEF2", floor="#BFA27E", sofa="#FF6B57", red="#E5383B", green="#2FA36B")
C = dict(  # Yön C — "Toprak Gouache"
  name="C · Toprak Gouache", paper="#FBF3E8", ink="#2B1D17",
  accent="#C8553D", accent2="#6B8F47", hide="#B8834A", hair="#4A2E22", hair2="#3A2A1F", shade="#EFE2D2", blush="#F08A6E",
  cap="#2F5D6B", nose="#E07A5F",
  sky="#F5DDB6", sky2="#FBEBD3", hill="#C9A46B", ground="#D9935A", ground2="#B66E3E", stone="#C7B29A", stone2="#9C8670",
  night="#22233F", night2="#3B3560", fire="#F4A23B", fire2="#FFE08A",
  wall="#F3D8BF", floor="#A8643B", sofa="#2F5D6B", red="#B83A2B", green="#6B8F47")
ALL = {"A": A, "B": B, "C": C}
