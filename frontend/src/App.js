import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { AppBar, Toolbar, Typography, Select, MenuItem, Badge, IconButton, Box, Button, TextField, Chip, List, ListItem, ListItemText, InputLabel, FormControl, OutlinedInput } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";

const API = "http://localhost:8000";

function App() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [ws, setWs] = useState(null);
  const [search, setSearch] = useState("");
  // Admin panel state
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");
  const [audience, setAudience] = useState("all");
  const [selectedRoles, setSelectedRoles] = useState([]);

  useEffect(() => {
    axios.get(`${API}/users`).then(res => setUsers(res.data));
    axios.get(`${API}/roles`).then(res => setRoles(res.data));
  }, []);

  useEffect(() => {
    if (currentUser) {
      axios.get(`${API}/notifications/${currentUser.id}`).then(res => {
        setNotifications(res.data);
        setUnreadCount(res.data.filter(n => !n.is_read).length);
      });
      // WebSocket for real-time
      const socket = new WebSocket(`ws://localhost:8000/ws/${currentUser.id}`);
      socket.onmessage = (event) => {
        const notif = JSON.parse(event.data);
        setNotifications(prev => [notif, ...prev]);
        setUnreadCount(prev => prev + 1);
      };
      setWs(socket);
      return () => socket.close();
    }
  }, [currentUser]);

  const handleUserChange = (e) => {
    const user = users.find(u => u.id === e.target.value);
    setCurrentUser(user);
  };

  const handleSend = async () => {
    let aud = audience === "all" ? "all" : selectedRoles.join(",");
    await axios.post(`${API}/notifications`, { title, message, audience: aud });
    setTitle(""); setMessage(""); setAudience("all"); setSelectedRoles([]);
  };

  const handleReadToggle = async (notif) => {
    await axios.post(`${API}/notifications/${notif.id}/read`, { user_id: currentUser.id, is_read: !notif.is_read });
    setNotifications(notifications.map(n => n.id === notif.id ? { ...n, is_read: !n.is_read } : n));
    setUnreadCount(notifications.filter(n => !n.is_read && n.id !== notif.id).length + (notif.is_read ? 1 : 0));
  };

  const filteredNotifications = notifications.filter(n =>
    n.title.toLowerCase().includes(search.toLowerCase()) ||
    n.message.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Box>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>NotifyHub</Typography>
          <FormControl sx={{ minWidth: 120, mr: 2 }}>
            <InputLabel>User</InputLabel>
            <Select
              value={currentUser ? currentUser.id : ""}
              onChange={handleUserChange}
              input={<OutlinedInput label="User" />}
            >
              {users.map(u => <MenuItem key={u.id} value={u.id}>{u.username} ({u.role})</MenuItem>)}
            </Select>
          </FormControl>
          <IconButton color="inherit">
            <Badge badgeContent={unreadCount} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>
      {currentUser && currentUser.role === "Admin" && (
        <Box sx={{ p: 2, border: "1px solid #ccc", m: 2, borderRadius: 2 }}>
          <Typography variant="h6">Admin Panel</Typography>
          <TextField label="Title" value={title} onChange={e => setTitle(e.target.value)} sx={{ mr: 2 }} />
          <TextField label="Message" value={message} onChange={e => setMessage(e.target.value)} sx={{ mr: 2 }} />
          <FormControl sx={{ minWidth: 120, mr: 2 }}>
            <InputLabel>Audience</InputLabel>
            <Select value={audience} onChange={e => setAudience(e.target.value)} label="Audience">
              <MenuItem value="all">All Users</MenuItem>
              <MenuItem value="roles">By Role</MenuItem>
            </Select>
          </FormControl>
          {audience === "roles" && (
            <FormControl sx={{ minWidth: 200, mr: 2 }}>
              <InputLabel>Roles</InputLabel>
              <Select
                multiple
                value={selectedRoles}
                onChange={e => setSelectedRoles(e.target.value)}
                input={<OutlinedInput label="Roles" />}
                renderValue={selected => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map(value => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                {roles.map(role => <MenuItem key={role} value={role}>{role}</MenuItem>)}
              </Select>
            </FormControl>
          )}
          <Button variant="contained" onClick={handleSend}>Send</Button>
        </Box>
      )}
      {currentUser && (
        <Box sx={{ p: 2, m: 2, border: "1px solid #eee", borderRadius: 2 }}>
          <Typography variant="h6">Notifications</Typography>
          <TextField label="Search" value={search} onChange={e => setSearch(e.target.value)} sx={{ mb: 2 }} />
          <List>
            {filteredNotifications.map(n => (
              <ListItem key={n.id} sx={{ bgcolor: n.is_read ? "#f5f5f5" : "#e3f2fd", mb: 1, borderRadius: 1 }}
                secondaryAction={
                  <Button onClick={() => handleReadToggle(n)} size="small">
                    {n.is_read ? "Mark Unread" : "Mark Read"}
                  </Button>
                }
              >
                <ListItemText
                  primary={<b>{n.title}</b>}
                  secondary={<>
                    <span>{n.message}</span><br />
                    <span style={{ fontSize: 12, color: '#888' }}>{new Date(n.created_at).toLocaleString()}</span>
                  </>}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );
}

export default App;
