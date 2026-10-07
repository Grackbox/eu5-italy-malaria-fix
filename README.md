# Italy Malaria Fix (EU5 mod)

Two small balance fixes for Europa Universalis V 1.4. Local mod, not on the Workshop.

- **Malaria in the Po valley.** 1.4 counts the valley as subtropical (x1.75) on wetlands (x3) with no resistance, which
  made it worse than tropical Africa. The eleven Po valley outbreak locations get a tenth of the infection; the rest of
  the world is unchanged. Overrides `in_game/common/diseases/malaria.txt`.
- **Nation State earlier.** From LudiMPbalance (Workshop 3664177503): the Nation State advance (Merge Culture Group
  cabinet action) moves from the Age of Revolutions to the Age of Reformation, after Fine Cloth Workshop.

`mod/` is the mod folder as it goes into `Documents/Paradox Interactive/Europa Universalis V/mod/italy_malaria_fix`.

## tools/fix_save_nation_state.py
A save keeps the advance tree it was started with, so the Nation State change doesn't reach running games. The script
moves the advance in a debug (text) save from the Age of Revolutions tree to the Age of Reformation tree:

```
python tools/fix_save_nation_state.py <save.eu5> <fixed.eu5>
```
